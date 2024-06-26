from pyrogram import Client, filters, types, enums
import requests


@Client.on_message(filters.command("repo"))
async def repo(client, message):
    # Split the message text and check if there are enough elements
    command_parts = message.text.split("/repo ", 1)
    if len(command_parts) > 1:
        query = command_parts[1]
        headers = {"Authorization": "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"}
        url = f"https://api.github.com/search/repositories?q={query}"
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            if "items" in data and len(data["items"]) > 0:
                repo = data["items"][0]
                repo_name = repo["full_name"]
                repo_url = repo["html_url"]
                fork_count = repo["forks_count"]
                repo_size = repo["size"] / 1024  # Convert size to KB
                language = repo["language"]
                repo_description = repo.get("description", "No description available")

                message_text = (
                    f"Repo: <b><i>{repo_name}</i></b>\n\n"
                    f"URL: <i>{repo_url}</i>\n\n"
                    f"Description: <b><i>{repo_description}</i></b>\n\n"
                    f"Language: <b><i>{language}</i></b>\n"
                    f"Size: {repo_size:.2f} KB\n"
                    f"Fork Count: {fork_count}"
                )

                await client.send_message(
                    message.chat.id,
                    text=message_text,
                    disable_web_page_preview=True,
                    parse_mode=enums.ParseMode.HTML  # Enable HTML formatting
                )
            else:
                await client.send_message(message.chat.id, "File not found.")
        else:
            await client.send_message(message.chat.id, "Processing...")
    else:
        await client.send_message(message.chat.id, "Processing...")
