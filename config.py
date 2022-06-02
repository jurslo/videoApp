# Copyright 2022 Juraj Sloboda
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Configuration file
"""

config = {
    # URL of REST API for video manifest
    'videos_manifest_url': 'https://gist.githubusercontent.com/nextsux/f6e0327857c88caedd2dab13affb72c1/raw/04441487d90a0a05831835413f5942d58026d321/videos.json',

    # Name of SQLight database file
    'database_name': 'video.db',

    # How often to sync data from video manifest REST API to local database (in seconds)
    'video_manifest_refresh_interval': 10*60
}
