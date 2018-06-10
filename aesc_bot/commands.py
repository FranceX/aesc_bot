# commands.py
# Project: aesc_bot
# 
# Created by "Francesco Servida"
# Created on 07.06.18

from aesc_bot.configuration import Configuration
from aesc_bot.utils import build_menu

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

# import requests
import bs4
# import html

from pprint import pprint

import feedparser

cantines = {
    "Amphimax": "amphimax",
    "Centre Sport et Santé": "css",
    "Geopolis": "geopolis",
    "Restaurant de Dorigny": "restaurant-de-dorigny",
    "Unithèque": "unitheque",
}


# start
def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id,
                     text="Ask me anything about the AESC activities!\n\n/help -> Display help")


# help
def help(bot, update):
    conf = Configuration.get_instance()
    bot.send_message(chat_id=update.message.chat_id,
                     text=conf.help)


def deadlines(bot, update):
    bot.send_message(chat_id=update.message.chat_id,
                     text="13 Juin - Rendu 1ere seance travaux de master\n11 Juillet - Rendu 2eme seance travaux de master")


# summer
def summer(bot, update):
    bot.send_message(chat_id=update.message.chat_id,
                     text="Summer! Barbecue Time!\nFête de fin d'année le 22 juin au parc bourget avec bière offerte et grillade!")


def parse_menu(cantine):
    feed = feedparser.parse("https://www2.unil.ch/menus/rss/menu-du-jour/{}".format(cantine))

    assiettes = {}
    if feed.get('entries', False):
        for assiette in feed['entries']:
            assiette_name = assiette['title'].split("-")[1].strip().replace(u'\xa0', ' ')
            assiette_contenu = "\n\t".join([line.strip() for line in
                                            bs4.BeautifulSoup(assiette['summary'], "html.parser").text.strip().strip(
                                                "\n").split("\n")])
            assiettes[assiette_name] = assiette_contenu
    else:
        assiettes = {"Informations pas disponibles": "Le restaurant est vraisamblablement fermé aujourd'hui"}

    return assiettes


def format_menu(assiettes):
    return "\n".join(
        ["*{}*:\n\t{}".format(assiette_name, assiette_contenu) for assiette_name, assiette_contenu in
         assiettes.items()])


def menu(bot, update):
    button_list = [InlineKeyboardButton(cantine, callback_data="menu_%s" % cantine_rss) for cantine, cantine_rss in
                   cantines.items()]

    reply_markup = InlineKeyboardMarkup(build_menu(button_list, n_cols=2))

    update.message.reply_text("Quelle cantine?", reply_markup=reply_markup)


def menu_handler(bot, update):
    query = update.callback_query
    cantine = query.data.replace("menu_", "")

    assiettes = parse_menu(cantine)

    bot.edit_message_text(chat_id=query.message.chat_id,
                          message_id=query.message.message_id,
                          text=format_menu(assiettes),
                          parse_mode='Markdown')


def version(bot, update):
    conf = Configuration.get_instance()
    bot.send_message(chat_id=update.message.chat_id,
                     text=conf.version)


# echo
def echo(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text=update.message.text)

