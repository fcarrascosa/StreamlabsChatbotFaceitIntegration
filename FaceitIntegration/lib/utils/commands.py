from ..actions.session import init_session, get_session_analysis, get_session_analysis_deprecated
from ..actions.elo import get_player_info

FUNCTION_PER_COMMAND = {
   'faceit_elo': get_player_info,
   # TODO: Replace this with get_session_analysis when FACEIT API gets FIXED
   'faceit_session': get_session_analysis_deprecated,
   'faceit_start_session': init_session
}
