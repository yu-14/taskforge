from app import clean, rank, score

assert clean("- [ ] I need to email prof") == "email prof"
assert clean("3) remember to pay rent") == "pay rent"

top, why = rank("finish the entire history project\nlaundry\n- email prof about extension ASAP\nread ch 4")[0]
assert top == "email prof about extension ASAP", top
assert "time-sensitive" in " ".join(why)

assert "clear action" in " ".join(score("Vacuum room")[1])            # expanded verb list
assert [t for t, _ in rank("groceries\nzzz stuff")] == ["groceries", "zzz stuff"]  # unknown verbs kept, typed order
assert rank("thesis\nvacuum room")[0][0] == "vacuum room"             # known verb still ranks higher
assert rank("   \n\n") == []
print("ok")
