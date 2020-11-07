from twython import Twython
import os

testapi = Twython(os.getenv("cons_key"), os.getenv("cons_secret"), os.getenv("access_token"), os.getenv("access_secret"))

print(testapi.lookup_user(screen_name="guitar_budgie")["id_str"])