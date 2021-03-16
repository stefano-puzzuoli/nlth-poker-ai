import React from 'react';

/**
 * Controller functional component which represents the base 
 * of the raise bar users can perform  call, fold or raise
 * actions through.
 */
function Controller({
  handle: { id, value, percent },
  getHandleProps
}) {
  return (
    <div
      style={{
        left: `${percent}%`,
        position: 'absolute',
        border: "3px solid #7177A3",
        textAlign: 'center',
        cursor: 'pointer',
        borderRadius: "25px",
        backgroundColor: '#FFEB49',
        marginLeft: -15,
        marginTop: 27,
        zIndex: 2,
        width: 30,
        height: 22,
      }}
      {...getHandleProps(id)}
    >
      <div style={{ display: 'flex', textShadow: '2px 2px 8px rgba(0,0,0,0.95)', justifyContent: 'center', fontFamily: 'Roboto', fontSize: 11, marginTop: 30 }} >
        {value}
      </div>
    </div>

  )
}

export default Controller;