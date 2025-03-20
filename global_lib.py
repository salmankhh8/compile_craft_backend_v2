import io
import sys
import math
import os
import random
import re
import string
import datetime
import time
import json
import logging
import collections
import queue
import socket
import urllib

global_namespace = {
    "math": math,
    "os": os,
    "random": random,
    "re": re,
    "string": string,
    "datetime": datetime,
    "time": time,
    "json": json,
    "logging": logging,
    "collections": collections,
    "queue": queue,
    "socket": socket,
    "urllib": urllib,
    "__builtins__": __builtins__
}