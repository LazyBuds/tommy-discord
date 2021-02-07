import discord
from discord.ext import commands
from pathlib import Path # For paths
import random
import asyncio
from typing import Optional
import requests
from aiohttp import ClientSession
import aiohttp
from ..db import db




class Covid(commands.Cog):
    """
    Covid API Commands!
    """



    def __init__(self, bot):
        self.bot = bot

    def custom_check():
        def predicate(ctx):
            cog = ctx.bot.get_cog("Fun") 
            command  =  db.field("SELECT commandname FROM command WHERE channelid = ?", ctx.channel.id)
            if command is not None:
                command.split(',')
                if  len(command)> 1 and ctx.command.name in command :
                    return 
                elif ctx.command.name in command :
                    return
            return True
        return commands.check(predicate)

    @commands.Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("covid")

    @commands.group(name = 'covid', description = 'show stats about covid-19', help= 'show stats about covid-19')
    @custom_check()
    async def covid(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send_help(str(ctx.command))
            


    @covid.group(name = 'country' ,description = 'Gets information of Covid-19 stats of a country', usage = '+covid country <country>')
    @custom_check()
    async def country(self, ctx, country1):
        
        try:

            url = f'https://disease.sh/v3/covid-19/countries/{country1}'
            async with ClientSession() as session:
                async with session.get(url) as response:
                    html = await response.json()
                    data = [html]

                    #getting data from API then format to readable numbers
                    test = data[0]["countryInfo"]["flag"]
                    population = data[0]["population"]
                    population_format = format(population, ",")
                    country = data[0]["country"]
                    cases = data[0]["cases"]
                    cases_format = format(cases, ",")
                    deaths = data[0]["deaths"]
                    deaths_format = format(deaths, ",")
                    active = data[0]["active"]
                    active_format = format(active, ",")
                    recovered = data[0]["recovered"]
                    recovered_format = format(recovered, ",")
                    critical = data[0]["critical"]
                    critical_format = format(critical, ",")
                    tests = data[0]["tests"]
                    tests_format = format(tests, ",")


                    #making stats
                    fatality = deaths/cases*100
                    fatality_rounded_value = round(fatality, 4)
                    fatality_rate_percent = "{}%".format(fatality_rounded_value)

                    infected = cases/population*100
                    infected_format = round(infected, 4)
                    infected_rate_percent = "{}%".format(infected_format)

                    critical_rate = critical/active*100
                    critical_rate_round = round(critical_rate, 4)
                    critical_rate_percent = "{}%".format(critical_rate_round)


                    recovered_rate = recovered/cases*100
                    recovered_rate_format = round(recovered_rate, 4)
                    recovered_rate_percent = "{}%".format(recovered_rate_format)

                    test_rate = tests/population*100
                    test_rate_format = round(test_rate, 4)
                    test_rate_percent = "{}%".format(test_rate_format)


                    # making embed
                    embed = discord.Embed(title=f'Covid Details: {country}')
                    embed.set_thumbnail(url=test)
                    embed.add_field(name='Total Cases', value=cases_format + '\u200b', inline=True)
                    embed.add_field(name='Total Deaths', value=deaths_format, inline=True)
                    embed.add_field(name='Active', value=active_format, inline=True)
                    embed.add_field(name='Recovered', value=recovered_format, inline=True)
                    embed.add_field(name='Critical', value=critical_format, inline=True)
                    embed.add_field(name='Tests', value=tests_format, inline=True)
                    embed.add_field(name='Population', value=population_format, inline=True)
                    embed.add_field(name='Infection Rate', value=infected_rate_percent, inline=True)
                    embed.add_field(name='Fatality Rate', value=fatality_rate_percent, inline=True)
                    embed.add_field(name='Critical Rate', value=critical_rate_percent, inline=True)
                    embed.add_field(name='Recovery Rate', value=recovered_rate_percent, inline=True)
                    embed.add_field(name='Test Rate', value=test_rate_percent, inline=True)
                    await ctx.send(embed=embed)

        except :
            await ctx.send('enter a valid country')

    @covid.group(name = 'all' , description = 'Gets Summary of All countries with Covid-19', usage = '+covid all')
    @custom_check()
    async def all(self, ctx):
        url = f'https://disease.sh/v3/covid-19/all'
        async with ClientSession() as session:
            async with session.get(url) as response:
                data = await response.json()

                #getting data from API then format to readable numbers
                case = data['cases']
                cases_format = format(case, ",")

                population = data["population"]
                population_format = format(population, ",")

                deaths = data["deaths"]
                deaths_format = format(deaths, ",")

                active = data["active"]
                active_format = format(active, ",")

                recovered = data["recovered"]
                recovered_format = format(recovered, ",")

                critical = data["critical"]
                critical_format = format(critical, ",")

                tests = data["tests"]
                tests_format = format(tests, ",")

                infected_countries = data['affectedCountries']


               


                #making stats
                fatality = deaths/case*100
                fatality_rounded_value = round(fatality, 4)
                fatality_rate_percent = "{}%".format(fatality_rounded_value)

                infected = case/population*100
                infected_format = round(infected, 4)
                infected_rate_percent = "{}%".format(infected_format)

                critical_rate = critical/active*100
                critical_rate_round = round(critical_rate, 4)
                critical_rate_percent = "{}%".format(critical_rate_round)


                recovered_rate = recovered/case*100
                recovered_rate_format = round(recovered_rate, 4)
                recovered_rate_percent = "{}%".format(recovered_rate_format)

                test_rate = tests/population*100
                test_rate_format = round(test_rate, 4)
                test_rate_percent = "{}%".format(test_rate_format)


                # making embed
                embed = discord.Embed(title=f'Covid Details All')
                embed.set_thumbnail(url='https://i2x.ai/wp-content/uploads/2018/01/flag-global.jpg')
                embed.add_field(name='Total Cases', value=cases_format + '\u200b', inline=True)
                embed.add_field(name='Total Deaths', value=deaths_format, inline=True)
                embed.add_field(name='Active', value=active_format, inline=True)
                embed.add_field(name='Recovered', value=recovered_format, inline=True)
                embed.add_field(name='Critical', value=critical_format, inline=True)
                embed.add_field(name='Tests', value=tests_format, inline=True)
                embed.add_field(name='Population', value=population_format, inline=True)
                embed.add_field(name='Infection Rate', value=infected_rate_percent, inline=True)
                embed.add_field(name='Fatality Rate', value=fatality_rate_percent, inline=True)
                embed.add_field(name='Critical Rate', value=critical_rate_percent, inline=True)
                embed.add_field(name='Recovery Rate', value=recovered_rate_percent, inline=True)
                embed.add_field(name='Test Rate', value=test_rate_percent, inline=True)
                embed.add_field(name='Infected Countries', value=infected_countries, inline=True)
                await ctx.send(embed=embed)

    @covid.group(name = 'continent',description= 'Gets Summary of a continent with Covid-19', usage = '+covid continent <continent>')
    @custom_check()
    async def continent(self, ctx, continent):
        try:

            url = f'https://disease.sh/v3/covid-19/continents/{continent}'
            async with ClientSession() as session:
                async with session.get(url) as response:
                    data = await response.json()

                    #getting data from API then format to readable numbers
                    case = data['cases']
                    cases_format = format(case, ",")

                    population = data["population"]
                    population_format = format(population, ",")

                    deaths = data["deaths"]
                    deaths_format = format(deaths, ",")

                    active = data["active"]
                    active_format = format(active, ",")

                    recovered = data["recovered"]
                    recovered_format = format(recovered, ",")

                    critical = data["critical"]
                    critical_format = format(critical, ",")

                    tests = data["tests"]
                    tests_format = format(tests, ",")

                    countries = data['countries']


                    #making stats
                    fatality = deaths/case*100
                    fatality_rounded_value = round(fatality, 4)
                    fatality_rate_percent = "{}%".format(fatality_rounded_value)

                    infected = case/population*100
                    infected_format = round(infected, 4)
                    infected_rate_percent = "{}%".format(infected_format)

                    critical_rate = critical/active*100
                    critical_rate_round = round(critical_rate, 4)
                    critical_rate_percent = "{}%".format(critical_rate_round)


                    recovered_rate = recovered/case*100
                    recovered_rate_format = round(recovered_rate, 4)
                    recovered_rate_percent = "{}%".format(recovered_rate_format)

                    test_rate = tests/population*100
                    test_rate_format = round(test_rate, 4)
                    test_rate_percent = "{}%".format(test_rate_format)


                    # making embed
                    embed = discord.Embed(title=f'Covid Details of {continent}')
                    embed.set_thumbnail(url='https://i2x.ai/wp-content/uploads/2018/01/flag-global.jpg')
                    embed.add_field(name='Total Cases', value=cases_format + '\u200b', inline=True)
                    embed.add_field(name='Total Deaths', value=deaths_format, inline=True)
                    embed.add_field(name='Active', value=active_format, inline=True)
                    embed.add_field(name='Recovered', value=recovered_format, inline=True)
                    embed.add_field(name='Critical', value=critical_format, inline=True)
                    embed.add_field(name='Tests', value=tests_format, inline=True)
                    embed.add_field(name='Population', value=population_format, inline=True)
                    embed.add_field(name='Infection Rate', value=infected_rate_percent, inline=True)
                    embed.add_field(name='Fatality Rate', value=fatality_rate_percent, inline=True)
                    embed.add_field(name='Critical Rate', value=critical_rate_percent, inline=True)
                    embed.add_field(name='Recovery Rate', value=recovered_rate_percent, inline=True)
                    embed.add_field(name='Test Rate', value=test_rate_percent, inline=True)
                    embed.add_field(name='Countries', value=countries, inline=True)

                    await ctx.send(embed=embed)

        except :
            await ctx.send('enter valid continent')

    # @covid.group(name  = 'india',description = 'Gets Summary of a indian state with Covid-19', usage = '+covid india <state>' )
    # async def india(self, ctx, *,state:str, district:str = None):
    #     try :
        
    #         url = requests.get("https://api.rootnet.in/covid19-in/unofficial/covid19india.org/statewise").json()
    #         data = url["data"]
    #         statewise = data["statewise"]
    #         state = state.lower()
    #         state = state.capitalize()
            
    #         states = [i for i in statewise if i["state"] == state]
            
    #         total = states[0]
            
    #         confirm = total["confirmed"]
    #         recover = total["recovered"]
    #         dead = total["deaths"]
    #         active = total["active"]
                
    #         embed=discord.Embed(title=f"**COVID-19 Statistics for {state}**" ,color=discord.Color.green())
    #         embed.add_field(name="Total cases: ",value=confirm)
    #         embed.add_field(name="Total recovered: ",value=recover)
    #         embed.add_field(name="Total deaths: ",value=dead)
    #         embed.add_field(name="Total active cases: ",value=active)
    #         await ctx.send(embed=embed)
                

    #     except :
    #         await ctx.send('enter a valid state or district')

    


    


        





def setup(bot):
    bot.add_cog(Covid(bot))
