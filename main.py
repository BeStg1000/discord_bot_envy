import os
import discord
from discord.ext import commands
from myserver import server_on

# เปิดใช้งาน Intents
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

# ตั้งค่า Client และ Command Tree สำหรับ Slash Commands
class MyBot(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tree = discord.app_commands.CommandTree(self)

bot = MyBot(intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    await bot.tree.sync()  # Sync Commands ไปยัง Discord Server

# เริ่มทำงานเซิร์ฟเวอร์ (จาก myserver)
server_on()

# ระบบจัดการ Role
@bot.tree.command(name="addrole", description="เพิ่ม role ให้กับผู้ใช้")
async def add_role(interaction: discord.Interaction, member: discord.Member, role_name: str):
    role = discord.utils.get(interaction.guild.roles, name=role_name)
    if role:
        await member.add_roles(role)
        await interaction.response.send_message(f"Added role {role_name} to {member.mention}")
    else:
        await interaction.response.send_message("Role not found.")

@bot.tree.command(name="removerole", description="ลบ role ของผู้ใช้")
async def remove_role(interaction: discord.Interaction, member: discord.Member, role_name: str):
    role = discord.utils.get(interaction.guild.roles, name=role_name)
    if role:
        await member.remove_roles(role)
        await interaction.response.send_message(f"Removed role {role_name} from {member.mention}")
    else:
        await interaction.response.send_message("Role not found.")

# ระบบจัดการ User
@bot.tree.command(name="kick", description="เตะผู้ใช้ออกจากเซิร์ฟเวอร์")
async def kick_user(interaction: discord.Interaction, member: discord.Member, reason: str = "No reason provided"):
    await member.kick(reason=reason)
    await interaction.response.send_message(f"{member.mention} has been kicked for: {reason}")

@bot.tree.command(name="ban", description="แบนผู้ใช้ออกจากเซิร์ฟเวอร์")
async def ban_user(interaction: discord.Interaction, member: discord.Member, reason: str = "No reason provided"):
    await member.ban(reason=reason)
    await interaction.response.send_message(f"{member.mention} has been banned for: {reason}")

# เริ่มต้นบอท
bot.run(os.getenv('TOKEN'))
