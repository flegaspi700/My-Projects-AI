""" Test script to see state access directly. Run with: python test_state.py """ 
import asyncio
from dotenv import load_dotenv 
load_dotenv() 

from agent import root_agent 
from google.adk.runners import Runner 
from google.adk.sessions import InMemorySessionService 
from google.genai.types import Content, Part 

async def main():
    # Setup Runner and Session 
    APP_NAME = "name_extractor_app"
    USER_ID = "test_user"
    SESSION_ID = "test_session"

    session_service = InMemorySessionService() 
    
    # Use the native async session creation method
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

    # Test 1: Extract name 
    user_message = Content(parts=[Part(text="Hi, my name is John Doe")]) 
    print("===Running Agent===") 
    
    # Use run_async to loop through events asynchronously
    async for event in runner.run_async( 
        user_id=USER_ID, 
        session_id=SESSION_ID, 
        new_message=user_message 
    ):
        if event.is_final_response() and event.content and event.content.parts: 
            print(f"\nAgent Response: {event.content.parts[0].text}") 

    # Retrieve the updated session object asynchronously
    session = await session_service.get_session(
        app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID
    )

    print(f"\n===State after execution===") 
    print(f"Full State: {session.state}") 
    print(f"Extracted Name: {session.state.get('user_name')}") 

    if session.state.get('user_name'): 
        print(f"Hello, {session.state.get('user_name')}! Nice to meet you.") 
    else: 
        print("Hello! I couldn't find your name in the message.") 

    # Test 2: Accessing in subsequent turns 
    print("\n===Simulating Subsequent Turn===") 
    
    async for event in runner.run_async( 
        user_id=USER_ID, 
        session_id=SESSION_ID, 
        new_message=Content(parts=[Part(text="Can you remember my name?")]) 
    ):
        if event.is_final_response() and event.content and event.content.parts: 
            print(f"\nAgent Response: {event.content.parts[0].text}") 

    # Retrieve final state snapshot
    session = await session_service.get_session(
        app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID
    )
    print(f"\nState still contains: {session.state.get('user_name')}") 
    print("State persists across turns!")

if __name__ == "__main__":
    asyncio.run(main())