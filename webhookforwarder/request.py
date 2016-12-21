from webhookforwarder.constants import OUTGOING


class Request:
    def __init__(self, token: str, team_id: str, team_domain: str, channel_id: str, channel_name: str, timestamp: str,
                 user_id: str, user_name: str, text: str, trigger_word: str = '', **extra):
        self.token = token
        self.team_id = team_id
        self.team_domain = team_domain
        self.channel_id = channel_id
        self.channel_name = channel_name
        self.timestamp = timestamp
        self.user_id = user_id
        self.user_name = user_name
        self.text = text
        self.trigger_word = trigger_word
        self.extra = extra

    @property
    def identity(self) -> str:
        return self.team_id + '/' + self.channel_id

    @classmethod
    def generate_request(cls, form):
        r = Request(token=form[OUTGOING.TOKEN], team_id=form[OUTGOING.TEAM_ID],
                    team_domain=form[OUTGOING.TEAM_DOMAIN], channel_id=form[OUTGOING.CHANNEL_ID],
                    channel_name=form[OUTGOING.CHANNEL_NAME], timestamp=form[OUTGOING.TIMESTAMP],
                    user_id=form[OUTGOING.USER_ID], user_name=form[OUTGOING.USER_NAME], text=form[OUTGOING.TEXT])
        if OUTGOING.TRIGGER_WORD in form:
            r.trigger_word = form[OUTGOING.TRIGGER_WORD]

        processed_keys = vars(OUTGOING).values()
        for k, v in form.items():
            if k not in processed_keys:
                r.extra[k] = v
        return r
