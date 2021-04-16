def should_check_command(data):
    return data.IsChatMessage() and is_from_streaming_platform(data)


def is_from_streaming_platform(data):
    return data.IsFromTwitch() or data.IsFromYoutube()
