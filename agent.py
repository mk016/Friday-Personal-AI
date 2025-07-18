from dotenv import load_dotenv

from livekit import agents
from livekit.agents import AgentSession, Agent, RoomInputOptions
from livekit.plugins import (
    noise_cancellation,
)
from livekit.plugins import google
from prompts import AGENT_INSTRUCTION, SESSION_INSTRUCTION
from tools import get_weather, search_web, send_email
from All_tools.tools_manager import get_all_tools, get_tools_description
from All_tools.screen_monitoring_advanced import (
    read_screen_content, read_browser_tab_content,
    monitor_active_application, find_text_on_screen
)
load_dotenv()


class Assistant(Agent):
    def __init__(self) -> None:
        super().__init__(
            instructions=f"""
You are Friday, a personal AI assistant like from Iron Man. You have access to various tools to help users.

Available Tools:
{get_tools_description()}

Always respond naturally and helpfully. If user speaks Hindi, respond in Hindi. If English, respond in English.
Use appropriate tools based on user requests.
"""
            ,
            llm=google.beta.realtime.RealtimeModel(
            voice="Aoede",
            temperature=0.8,
        ),
            tools=get_all_tools(),

        )
        
    def setup_tools(self):
        """Setup all available tools"""
        tools = get_all_tools()
        self.register_tools(tools)
        
        # Update instructions with tools description
        tools_desc = get_tools_description()
        self.config.instructions += f"\n\nAvailable Tools:\n{tools_desc}"


async def entrypoint(ctx: agents.JobContext):
    session = AgentSession(
        
    )

    await session.start(
        room=ctx.room,
        agent=Assistant(),
        room_input_options=RoomInputOptions(
            # LiveKit Cloud enhanced noise cancellation
            # - If self-hosting, omit this parameter
            # - For telephony applications, use `BVCTelephony` for best results
            video_enabled=True,
            noise_cancellation=noise_cancellation.BVC(),
        ),
    )

    await ctx.connect()

    await session.generate_reply(
        instructions=SESSION_INSTRUCTION,
    )


if __name__ == "__main__":
    agents.cli.run_app(agents.WorkerOptions(entrypoint_fnc=entrypoint))