import React from 'react';

/**
 * Card component which represents the private Poker game cards 
 * dealt to the User and the Community cards dealt on the table.
 */
const Card = (props) => {
  const {
    cardData: {
      suit,
      cardFace,
    }
  } = props;

  // get suit of card
  var suitOfCard = suit.substring(0, 1).toUpperCase();

  // display card according to value and suit given
  return (
    <div className="poker-card"><img src={`${process.env.PUBLIC_URL}/assets/cardFaces/${cardFace}${suitOfCard}.svg`}></img></div>
  )
}

export default Card;