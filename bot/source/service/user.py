from repository.user import UserRepository

class UserService:
    def __init__(self, userRepository : UserRepository):
        self.userRepository = userRepository

    def save(self, user):
        self.userRepository.save(user)

    def get(self, userid):
        return self.userRepository.get_from_telegram(userid)
