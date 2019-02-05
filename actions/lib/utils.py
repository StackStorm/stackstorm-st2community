# Licensed to the StackStorm, Inc ('StackStorm') under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from datetime import timedelta

__all__ = [
    'get_timedelta_object_from_delta_arg'
]

def get_timedelta_object_from_delta_arg(delta):
    time_delta = timedelta(
            days=delta.get('days', 0),
            hours=delta.get('hours', 0),
            minutes=delta.get('minutes', 0),
            seconds=delta.get('seconds', 0)
        )

    return time_delta
