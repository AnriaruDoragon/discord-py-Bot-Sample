import discord

def GetEntireContent(message:discord.Message):
    content = message.content.lower().replace(" ", "")
    if len(message.embeds) > 0:
        for embed in message.embeds:
            embed = embed.to_dict()
            if "footer" in embed:
                if "text" in embed["footer"]:
                    content += " " + embed["footer"]["text"].lower().replace(" ", "")
                if "icon_url" in embed["footer"]:
                    content += " " + embed["footer"]["icon_url"].lower().replace(" ", "")
            if "image" in embed:
                content += " " + embed["image"]["url"].lower().replace(" ", "")
            if "thumbnail" in embed:
                content += " " + embed["thumbnail"]["url"].lower().replace(" ", "")
            if "author" in embed:
                if "url" in embed["author"]:
                    content += " " + embed["author"]["url"].lower().replace(" ", "")
                if "name" in embed["author"]:
                    content += " " + embed["author"]["name"].lower().replace(" ", "")
                if "icon_url" in embed["author"]:
                    content += " " + embed["author"]["icon_url"].lower().replace(" ", "")
            if "fields" in embed:
                for field in embed["fields"]:
                    if "value" in field:
                        content += " " + field["value"].lower().replace(" ", "")
                    if "name" in field:
                        content += " " + field["name"].lower().replace(" ", "")
            if "description" in embed:
                    content += " " + embed["description"].lower().replace(" ", "")
            if "url" in embed:
                    content += " " + embed["url"].lower().replace(" ", "")
            if "title" in embed:
                content += " " + embed["title"].lower().replace(" ", "")
    return content

def SplitString(text:str, size:int = 2000):
    return [text[chunk:chunk+size] for chunk in range(0, len(text), size)]
