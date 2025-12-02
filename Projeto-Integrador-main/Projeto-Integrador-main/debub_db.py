import supabase_helpers
import database

print("SUPABASE_URL =", supabase_helpers.SUPABASE_URL)
print("SUPABASE_KEY OK =", bool(supabase_helpers.SUPABASE_KEY))
print("SUPABASE CLIENTE OK =", supabase_helpers.supabase is not None)

print("__all__ em database =", database.__all__)
