import string
import random

async def random_wallet_code():
   letters = string.ascii_letters + string.digits

   return ''.join(random.choice(letters) for i in range(32))

