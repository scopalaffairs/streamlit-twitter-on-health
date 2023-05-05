# Convert column to string type
df_dict[frame]["analyseEmotion"] = df_dict[frame]["translatedContent"].astype(str)

# Classify the dataframe
df_dict[frame]["analyseEmotion"] = df_dict[frame]["translatedContent"].apply(
    analyse_emotion
)
df_dict[frame]["location"] = df_dict[frame].user.apply(lambda x: x["location"])

# Save to files
df_dict[frame].to_json(
    f"./data-emotions/processed_{frame}.json", orient="records", lines=True
)
