import random 
import time

#Initial Market state

mid_price=1000.00

def generate_market_event(event_id):
  global mid_price

  #Simulate price movement
  movement = random.choice([-0.10,-0.05,0.00,0.05,0.10])#spread can be anyone of these for the simulation

  mid_price=round(mid_price+movement,2)#price move according to the spread rounding off to 2 decimals

  #generate the bid and ask

  bid=round(mid_price-0.10,2)
  ask=round(mid_price+0.10,2)

#Generate market quantities

  bid_quantity=random.randint(100,1000)
  ask_quantity=random.randint(100,1000)


#Calculate Spread
  spread=round(ask-bid,2)

  return {
    "event_id":event_id,
    "timestamp":time.time(),
    "mid_price":mid_price,
    "bid":bid,
    "ask":ask,
    "spread":spread,
    "bid_qty":bid_quantity,
    "ask_qty":ask_quantity
  }


if __name__ == "__main__":
  for event_id in range(1,21):
    event= generate_market_event(event_id)
    print(event)
    time.sleep(0.2)