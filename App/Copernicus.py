import os
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
import numpy as np
from PIL import Image
import geopandas as gpd
import io


class Copernicus(object):

    def download_image(self):
        path = str((os.path.dirname(os.path.abspath(__file__)))) + "\\" + "file.geojson"
        bbox = gpd.read_file(path)
        coord = np.dstack(bbox.geometry[0].exterior.coords.xy).tolist()

        with open("credential.txt") as f:
            lines = f.readlines()
            client_id = lines[0].strip()
            client_secret = lines[1].strip()

        # set up credentials
        client = BackendApplicationClient(client_id=client_id)
        oauth = OAuth2Session(client=client)

        # get an authentication token
        try:
            token = oauth.fetch_token(token_url='https://services.sentinel-hub.com/oauth/token',
                                      client_id=client_id, client_secret=client_secret)
        except:
            return 123

        json_request = {
            "input": {
                "bounds": {
                    "geometry": {
                        "coordinates": coord,
                        "type": "Polygon"
                    }
                },
                "data": [
                    {
                        "dataFilter": {
                            "timeRange": {
                                "from": "2022-08-04T00:00:00Z",
                                "to": "2022-12-04T23:59:59Z"
                            },

                            "mosaickingOrder": "leastCC",
                            "maxCloudCoverage": "0"
                        },
                        "type": "sentinel-2-l2a",

                    }
                ]
            },
            "output": {

                "width": 512,
                "height": 272.633,
                "responses": [
                    {

                        "identifier": "default",
                        "format": {
                            "type": "image/png"
                        }
                    }
                ]
            },
            "evalscript": "//VERSION=3\n\nfunction setup() {\n  return {\n    input: [\"B02\", \"B03\", \"B04\"],\n    output: { bands: 3 }\n  };\n}\n\nfunction evaluatePixel(sample) {\n  return [2.5 * sample.B04, 2.5 * sample.B03, 2.5 * sample.B02];\n}"
        }

        # Set the request url and headers
        url_request = 'https://services.sentinel-hub.com/api/v1/process'
        headers_request = {
            "Authorization": "Bearer %s" % token['access_token']
        }

        # Send the request
        response = oauth.request(
            "POST", url_request, headers=headers_request, json=json_request
        )

        sentence = str(response.content)
        word = 'error'
        if word in sentence:
            im = None

            if '400' in sentence:
                im = 400
            if '403' in sentence:
                im = 403

            return im

        im = Image.open(io.BytesIO(response.content))
        im.save("cop_img.png")
        return im
