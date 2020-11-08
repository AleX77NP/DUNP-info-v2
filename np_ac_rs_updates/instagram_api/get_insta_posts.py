import requests
import json
import pprint
import os

module_dir = os.path.dirname(__file__)
TOKEN_PATH = os.path.join(module_dir, 'token.txt')

ALL_POSTS_URL = 'https://graph.instagram.com/me/media?fields=id&access_token='

def get_access_token():
	with open(TOKEN_PATH, 'r') as token_file:
		return token_file.read()


def get_posts_dict(access_token):
	posts_response = requests.get(ALL_POSTS_URL + access_token)
	posts = json.loads(posts_response.text)['data']
	return posts


def form_post_url(post_id, access_token):
	return f'https://graph.instagram.com/{post_id}?fields=timestamp,permalink,caption&access_token={access_token}'


def get_new_posts(id_postova_kojih_nema_u_bazi, access_token):
	posts = []
	for post_id in id_postova_kojih_nema_u_bazi:
		post_response = requests.get(form_post_url(post_id, access_token))
		caption = json.loads(post_response.text).get('caption', '')
		permalink = json.loads(post_response.text)['permalink'].replace('\\', '')
		timestamp = json.loads(post_response.text)['timestamp']
		type_post = 'instagram'
		posts.append({
			'id': post_id, 
			'tip': type_post, 
			'link': permalink, 
			'naslov': caption,
			'opis': caption,
			'datum': timestamp
		})
	return posts


# Prima listu id-eva svih instagram novosti u bazi, i vraca listu novih instagram obavestenja
def uzmi_sve_nove_instagram_postove(id_postova_u_bazi):
	access_token = get_access_token()
	posts_dict = get_posts_dict(access_token)
	# Uzimam id svih postova kojih nema u bazi
	id_postova_kojih_nema_u_bazi = [x['id'] for x in posts_dict if  not x['id'] in  id_postova_u_bazi]
	# Uzimam sadrzaj novih postova
	novi_postovi = get_new_posts(id_postova_kojih_nema_u_bazi, access_token)

	return novi_postovi


if __name__ == "__main__":  # test 
	posts = uzmi_sve_nove_instagram_postove(['17879914003696839', '17855795162088381', '17881437862677384'])
	pprint.pprint(posts)

