import requests
import logging

class Harvest:
	USERAGENT = "Harvest API python playground (harvest@feuerrot.org)"
	BASEURL = "https://api.harvestapp.com/api"

	def __init__(self, access_token, account_id):
		self.token = access_token
		self.account = account_id
		self.session = requests.Session()
		self.__init_session()

	def debug(self):
		import http.client as http_client
		http_client.HTTPConnection.debuglevel = 1

		logging.basicConfig()
		logging.getLogger().setLevel(logging.DEBUG)
		requests_log = logging.getLogger("requests.packages.urllib3")
		requests_log.setLevel(logging.DEBUG)
		requests_log.propagate = True

	def __init_session(self):
		update = {
			"Authorization": "Bearer {}".format(self.token),
			"Harvest-Account-Id": str(self.account),
			"User-Agent": self.USERAGENT
		}
		self.__update_headers(update)

	def __update_headers(self, headers):
		self.session.headers.update(headers)

	def _get(self, path, version=2, page=1):
		url = "{}/v{}/{}".format(
			self.BASEURL,
			version,
			path
		)
		req = self.session.get(url, params={"page": page})
		req.raise_for_status()

		return req.json()

	def __get_pagedata(self, data):
		return (data["page"], data["total_pages"])

	def depaginate(self, element_name, request):
		data = []
		page = 1

		while True:
			req = request(element_name, page=page)
			data += req[element_name]
			(page, pages) = self.__get_pagedata(req)
			if page == pages:
				break
			page += 1

		return data

	def time_entries(self):
		data = self.depaginate("time_entries", self._get)
		return data
