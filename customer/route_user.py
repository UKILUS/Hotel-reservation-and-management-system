#-*- coding:utf-8 -*-
# author: Liangxinyu
# datetime:2022/1/4 18:02

from flask import Blueprint, request, render_template, session, redirect
from .db_user import *
from utils import *
import json
user = Blueprint("user", __name__)

@user.route("/", methods=['GET', 'POST'], endpoint='index')
def index():


    return render_template('index.html', user=user)
