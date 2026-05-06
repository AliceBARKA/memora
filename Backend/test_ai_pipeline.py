from ai_service.pipeline import generate_flashcards_pipeline

text = """
TCP is a connection-oriented protocol.
It guarantees delivery and order of packets.
UDP is connectionless and faster, but it does not guarantee delivery.
"""

cards = generate_flashcards_pipeline(text)

print(cards)