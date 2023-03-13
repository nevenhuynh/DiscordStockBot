import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from yahooquery import Ticker
import matplotlib.pyplot as plt

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')


stocks = ['AAPL', 'AC', 'AMZN', 'CADUSD=X', 'DKNG', 'GOOG', 'HIVE', 'META', 'MFST', 'NNDM', 'PLTR', 'TSLA', '^GSPC']

if not os.path.exists("images"):
    """
    create directory for storing plot image
    """
    os.mkdir("images")


@bot.command()
async def info(ctx):
    """
    Shows the user all the available commands
    :param ctx: ctx
    :return: commands
    """
    await ctx.send(
        'use !stock {ticker symbol} to view the stock price '
        '\n use !show to view a list of the stocks available on Stock bot'
        '\n use !history {ticker symbol} to view the stock price over the last year')


@bot.command()
async def show(ctx):
    """
    Sends the chat a message of a list of available stocks
    :param ctx: ctx
    :return: list of stocks
    """
    await ctx.send(', '.join(stocks))


@bot.command()
async def stock(ctx, arg1):
    """
    Sends the chat a message containing financial data of the inputted ticker symbol
    :param ctx: ctx
    :param arg1: ticker symbol
    :return: returns either a message that the inputted ticker is invalid or the ticker's financial data
    """
    if arg1 in stocks:
        ticker = Ticker(arg1)
    else:
        await ctx.send(arg1 + ' is not a valid ticker')

    await ctx.send(ticker.financial_data)


@bot.command()
async def history(ctx, arg1):
    """
    Sends the chat an image of the price history of the inputted ticker symbol
    :param ctx: ctx
    :param arg1: ticker symbol
    :return: returns a png of a plot of the price history
    """
    if arg1 in stocks:
        ticker = Ticker(arg1)
    else:
        await ctx.send(arg1 + ' is not a valid ticker')
    data = ticker.history(period='1y', interval='1mo')

    column = data.loc[:, 'close']
    column = column.reset_index(level=[0])

    column.plot()
    plt.grid()
    plt.legend().remove()
    plt.xlabel('Date')
    plt.ylabel('Price in USD')
    plt.title(arg1 + ' price over the last year')

    plt.savefig('images/stock_year.png')
    await ctx.send(file=discord.File('images/stock_year.png'))

    os.remove('images/stock_year.png')


if __name__ == "__main__":
    bot.run(TOKEN)
