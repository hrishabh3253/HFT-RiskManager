from market_simulator import generate_market_event

def generate_quotes(event):#event is the market data dictionary passed into the function
  mid_price=event["mid_price"]
  #distance from mid-price
  quote_offset = 0.05
  our_bid=round(mid_price-quote_offset,2)#bid price calculated by market maker
  our_ask=round(mid_price+quote_offset,2)#ask price calculate by market maker

  return{
    "event_id":event["event_id"],
    "market_mid":mid_price,
    "our_bid":our_bid,
    "our_ask":our_ask,
    "our_spread":round(our_ask-our_bid,2)
  }

if __name__=="__main__":
  for event_id in range(1,11):
    market_event=generate_market_event(event_id)
    quotes=generate_quotes(market_event)

    print(
       f"Event {quotes['event_id']:02d} | "
            f"Mid: {quotes['market_mid']:.2f} | "
            f"Our Bid: {quotes['our_bid']:.2f} | "
            f"Our Ask: {quotes['our_ask']:.2f} | "
            f"Our Spread: {quotes['our_spread']:.2f}"
    )
