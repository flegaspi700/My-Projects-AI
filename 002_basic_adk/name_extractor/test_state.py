"""
Test script to see state accessdirectly.
Run with: python test_state.py

"""

from agent import root_agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai.types import Content, Part

#Setup Runner and Session
session_service = InMemorySessionService()
session = session_service.create_session_sync(
    app_name="name_extractor_app",
    user_id="test_user",
    session_id="test_session"
)

runner = Runner(
    agent=root_agent,
    app_name="name_extractor_app",
    session_service=session_service
)

# Test: Extract name
user_message = Content(parts=[Part(text="Hi, my name is John Doe")])

print("===Running Agent===")
result = runner.run(
    user_id="test_user",
    session_id="test_session",
    new_message=user_message
)

#show final response
for event in result:
    if event.is_final_response():
        print(f"\nAgent Response: {event.content.parts[0].text}")


#Access state programmatically
print(f"\n===State after execution===")
print(f"Full State: {session.state}")
print(f"Extracted Name: {session.state.get('user_name')}")

#your code can now make decisions based on the state
if session.state.get('user_name'):
    print(f"Hello, {session.state.get('user_name')}! Nice to meet you.")
else:
    print("Hello! I couldn't find your name in the message.")

# Test accessing in subsequent turns
print("\n===Simulating Subsequent Turn===")
result2 = runner.run(
    user_id="test_user",
    session_id="test_session",
    new_message=Content(parts=[Part(text="Can you remember my name?")])
)

for event in result2:
    if event.is_final_response():
        print(f"\nAgent Response: {event.content.parts[0].text}")

print(f"\nState still contains: {session.state.get('user_name')}")
print("State persists across turns!")