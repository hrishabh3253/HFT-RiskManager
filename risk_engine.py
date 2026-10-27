class riskengine:
  def __init__(self,max_position=500,  max_loss=5000):
    self.position=0
    self.max_position=max_position
    self.max_loss=max_loss
    self.realized_pnl=0.0


  def check_order(self,side,quantity):
    if side =="BUY":
      proposed_position=self.position+quantity
    elif side =="SELL":
      proposed_position= self.position-quantity
    else:
      return False, "INVALID SIDE"
  #checking the position if we crossed the position over max_position
    if abs(proposed_position)>self.max_position:
      return False, "Position Limit Breached"
    else:
      return True, "Order Approved"

  def update_position(self,side,filled_qty):
    if side=="BUY":
      self.position += filled_qty
    elif side =="SELL":
      self.position -= filled_qty

  def check_loss(self,pnl):
    if pnl <= -self.max_loss:
      return False, "Limit Breached"
    else:
      return True," Loss limit is not breached yet"



    
    
if __name__ == "__main__":
    risk = riskengine(max_position=500, max_loss=5000)

    approved, message = risk.check_order("BUY", 300)
    print(message)

    if approved:
        risk.update_position("SELL", 100)

    print("Current position:", risk.position)

    approved, message = risk.check_order("BUY", 250)
    print(message)

    pnl = -5200
    approved, message = risk.check_loss(pnl)
    print(message)

