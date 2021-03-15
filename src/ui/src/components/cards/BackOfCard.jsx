import React from 'react';

/**
 * Back of Card component which represents the private Poker game cards 
 * dealt to AI players which remain hidden from the user.
 */
const BackOfCard = (props) => {
  const {
    cardData: {
      suit,
      cardFace,
      stallAnimation
    },
    setFoldedClassName
  } = props;

  // display back of card (values hidden from user)
  return (
    <div
      key={`${suit} ${cardFace}`}
      className={`poker-card cardIn agent-card${(setFoldedClassName ? ' folded' : '')}`}
      style={{ stallAnimation: `${(setFoldedClassName) ? 0 : stallAnimation}ms` }}>
    </div>
  )
}

export default BackOfCard;