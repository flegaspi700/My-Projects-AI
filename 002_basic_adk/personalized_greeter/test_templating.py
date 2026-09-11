"""
Test state templating with different state values.

Run with: python test_templating.py
"""
from agent import root_agent
from dotenv import load_dotenv
load_dotenv()
import asyncio

from google.adk.events import Event, EventActions
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai.types import Content, Part

async def main():
    #setup Runner and Session
    APP_NAME = "greeter_app"
    USER_ID = "user1"
    SESSION_ID = "session1"

    #create session service instance
    session_service = InMemorySessionService()

    await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=SESSION_ID
    )

    runner = Runner(
        agent=root_agent,
        app_name=APP_NAME,
        session_service=session_service
    )

    # Test 1: No state set (all defaults)
    print("===Test 1: No state set (all defaults)===")
    result1 = runner.run(
        user_id=USER_ID,
        session_id=SESSION_ID,
        new_message=Content(parts=[Part(text="Hello!")])
    )

    for event in result1:
        if event.is_final_response(): #and event.content and event.content.parts:
            print(f"\nAgent: {event.content.parts[0].text}")

    # Retrieve the updated session object asynchronously
    session = await session_service.get_session(
        app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID
    )

    # Test 2: Set user name only
    print("=== Test 2: With user name===")
    #session.state["user_name"] = "Alex" -- This doesn't work anymore
    # Create an event action specifying the state changes you want to apply
    await session_service.append_event(
    session,
    Event(
        invocation_id="manual-state-update",
        author="test",
        actions=EventActions(
            state_delta={"user_name": "Alex"}
        ),
    ),
    )

    # Run the second turn using the exact same session IDs    
    result2 = runner.run(
            user_id=USER_ID,
            session_id=SESSION_ID,
            new_message=Content(parts=[Part(text="Hello again!")])
        )

    for event in result2:
        if event.is_final_response(): #and event.content and event.content.parts:
            print(f"\nAgent: {event.content.parts[0].text}")
    
    print("===Current State===")
    print(session.state)

if __name__ == "__main__":
    asyncio.run(main())