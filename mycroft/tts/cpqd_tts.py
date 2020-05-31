# Copyright 2017 Mycroft AI Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from .tts import TTS, TTSValidator
from mycroft.configuration import Configuration
from requests.auth import HTTPBasicAuth
from requests import post
import json
from mycroft.util.log import LOG


class CPqDTTS(TTS):
    """
        Interface to CPqD TTS.
        https://speechweb.cpqd.com.br/tts/docs/latest/ProgrammingGuide/Rest
        Add configuration to local mycroft.conf file. The STT config will
        look like this:
        "tts": {
            "module": "cpqd",
            "cpqd": {
            "url": "http://127.0.0.1:9090/rest/v2/synthesize"
            }
        }
    """

    def __init__(self, lang, config):
        super(CPqDTTS, self).__init__(lang, config, CPqDTTSValidator(self))
        self.url = self.config.get("url")
        self.voice = self.config.get("voice", None)

    def get_tts(self, sentence, wav_file):
        data = {"text": sentence}
        if self.voice:
            data['voice'] = self.voice

        headers = {"Content-Type": "application/json",
                   "Accept": "audio/x-wav "}

        response = post(self.url, headers=headers,
                        data=json.dumps(data))
        LOG.debug("Response cpqd-tts: " + str(response.status_code))
        if response.status_code == 200:
            with open(wav_file, "wb") as f:
                f.write(response.content)
            return (wav_file, None)
        else:
            raise Exception(
                'Request to CPqD-TTS Server failed. Code: {}'.format(
                    response.status_code))


class CPqDTTSValidator(TTSValidator):
    def __init__(self, tts):
        super(CPqDTTSValidator, self).__init__(tts)

    def validate_dependencies(self):
        # TODO
        pass

    def validate_lang(self):
        # TODO
        pass

    def validate_connection(self):
        # TODO
        pass

    def get_tts_class(self):
        return CPqDTTS
