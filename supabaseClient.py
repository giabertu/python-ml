import os
from supabase import create_client, Client

url: str = 'https://drxkhmuiheyogtzbktoq.supabase.co'
key: str = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRyeGtobXVpaGV5b2d0emJrdG9xIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MDg5NjU2NzUsImV4cCI6MjAyNDU0MTY3NX0.nybBNviS2Oy0mUcXwco8YX8yINFwMxVDRRPT9HGgShg'

supabase: Client = create_client(url, key)
