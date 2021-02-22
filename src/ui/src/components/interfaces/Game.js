import 'core-js/es/array';
import 'core-js/es/map';
import 'core-js/es/set';
import "core-js/stable";
import { cloneDeep } from 'lodash';
import 'raf/polyfill';
import React, { Component } from 'react';
import { Dropdown, DropdownButton } from 'react-bootstrap';
import { Link } from "react-router-dom";
import "regenerator-runtime/runtime";
import '../../App.css';
import '../../Game.css';
import {
  aiHandler as aiHandlerUtil
} from '../../services/aiService.js';
import {
  anteUpBlinds, calculateBlindIndices,

  calculateMinBet,
  manageBet,
  managePlayerFold
} from '../../services/betService.js';
import {
  dealPlayerCards, makeDeckOfCards,
  shuffleCards
} from '../../services/cardsService.js';
import {
  checkWin, makeTable, startNextRound
} from '../../services/playersService.js';
import {
  makeActionButtonText,

  makeActionMenu, makeNetPlayerEarnings, makeShowdownMessages
} from '../../services/uiService.js';
import Card from "../cards/Card";
import SpinnerLoading from '../helpers/SpinnerLoading';
import Player from "../players/Player";
import PlayerShowdown from "../players/PlayerShowdown";
import PlayerWin from './PlayerWin';

/**
 * Game component to allow user to play Poker against
 * Ai Agents at a table until there is a winner.
 */
class Game extends Component {
  state = {
    loading: true,
    winnerFound: null,
    winner: null,
    players: null,
    numPlayersActive: null,
    numPlayersFolded: null,
    numPlayersAllIn: null,
    activePlayerIndex: null,
    dealerIndex: null,
    blindIndex: null,
    deck: null,
    communityCards: [],
    pot: null,
    highBet: null,
    betInputValue: null,
    sidePots: [],
    minBet: 20,
    phase: 'loading',
    playerHierarchy: [],
    showDownMessages: [],
    playActionMessages: [],
    playerAnimationSwitchboard: {
      0: { isAnimating: false, content: null },
      1: { isAnimating: false, content: null },
      2: { isAnimating: false, content: null },
      3: { isAnimating: false, content: null },
      4: { isAnimating: false, content: null },
      5: { isAnimating: false, content: null }
    }
  }

  cardAnimationDelay = 0;

  async componentDidMount() {
    const players = await makeTable();
    const dealerIndex = Math.floor(Math.random() * Math.floor(players.length));
    const blindIndicies = calculateBlindIndices(dealerIndex, players.length);
    const playersBoughtIn = anteUpBlinds(players, blindIndicies, this.state.minBet);

    const imageLoaderRequest = new XMLHttpRequest();

    imageLoaderRequest.addEventListener("load", e => {
      console.log(`${e.type}`);
      console.log(e);
      console.log("Image Loaded!");
      this.setState({
        loading: false,
      })
    });

    imageLoaderRequest.addEventListener("error", e => {
      console.log(`${e.type}`);
      console.log(e);
    });


    imageLoaderRequest.addEventListener("loadstart", e => {
      console.log(`${e.type}`);
      console.log(e);
    });

    imageLoaderRequest.addEventListener("loadend", e => {
      console.log(`${e.type}`);
      console.log(e);
    });

    imageLoaderRequest.addEventListener("abort", e => {
      console.log(`${e.type}`);
      console.log(e);
    });

    imageLoaderRequest.addEventListener("progress", e => {
      console.log(`${e.type}`);
      console.log(e);
    });

    imageLoaderRequest.open("GET", "./assets/table.svg");
    imageLoaderRequest.send();

    this.setState(prevState => ({
      // loading: false,
      players: playersBoughtIn,
      numPlayersActive: players.length,
      numPlayersFolded: 0,
      numPlayersAllIn: 0,
      activePlayerIndex: dealerIndex,
      dealerIndex,
      blindIndex: {
        big: blindIndicies.bigBlindIndex,
        small: blindIndicies.smallBlindIndex,
      },
      deck: shuffleCards(makeDeckOfCards()),
      pot: 0,
      highBet: prevState.minBet,
      betInputValue: prevState.minBet,
      phase: 'initialDeal',
    }))
    this.executeGame();
  }

  executeGame = () => {
    const newState = dealPlayerCards(cloneDeep(this.state))
    this.setState(newState, () => {
      if ((this.state.players[this.state.activePlayerIndex].robot) && (this.state.phase !== 'showdown')) {
        setTimeout(() => {
          this.aiHandler()
        }, 1200)
      }
    })
  }

  aiHandler = () => {
    const { playerAnimationSwitchboard, ...appState } = this.state;
    const newState = aiHandlerUtil(cloneDeep(appState), this.changePlayerAnimationState)

    this.setState({
      ...newState,
      betInputValue: newState.minBet
    }, () => {
      if ((this.state.players[this.state.activePlayerIndex].robot) && (this.state.phase !== 'showdown')) {
        setTimeout(() => {

          this.aiHandler()
        }, 1200)
      }
    })
  }

  manageBetChange = (val, min, max) => {
    if (val === '') val = min
    if (val > max) val = max
    this.setState({
      betInputValue: parseInt(val, 10),
    });
  }

  manageBetSubmit = (bet, min, max) => {
    const { playerAnimationSwitchboard, ...appState } = this.state;
    const { activePlayerIndex } = appState;
    this.changePlayerAnimationState(activePlayerIndex, `${makeActionButtonText(this.state.highBet, this.state.betInputValue, this.state.players[this.state.activePlayerIndex])} ${(bet > this.state.players[this.state.activePlayerIndex].bet) ? (bet) : ""}`);;
    const newState = manageBet(cloneDeep(appState), parseInt(bet, 10), parseInt(min, 10), parseInt(max, 10));
    this.setState(newState, () => {
      if ((this.state.players[this.state.activePlayerIndex].robot) && (this.state.phase !== 'showdown')) {
        setTimeout(() => {

          this.aiHandler()
        }, 1200)
      }
    });
  }

  manageSliderInputChange = (val) => {
    this.setState({
      betInputValue: val[0]
    })
  }

  managePlayerFold = () => {
    const { playerAnimationSwitchboard, ...appState } = this.state
    const newState = managePlayerFold(cloneDeep(appState));
    this.setState(newState, () => {
      if ((this.state.players[this.state.activePlayerIndex].robot) && (this.state.phase !== 'showdown')) {
        setTimeout(() => {

          this.aiHandler()
        }, 1200)
      }
    })
  }

  manageNextRound = () => {
    this.setState({ clearCards: true })
    const newState = startNextRound(cloneDeep(this.state))
    var winner;
    // Check win condition
    if (checkWin(newState.players)) {
      const players = newState.players
      players.forEach(element => {
        if (element.chips > 0)
          winner = element
      });
      this.setState({ winner: winner });
      this.setState({ winnerFound: true })

      return;
    }
    this.setState(newState, () => {
      if ((this.state.players[this.state.activePlayerIndex].robot) && (this.state.phase !== 'showdown')) {
        setTimeout(() => this.aiHandler(), 1200)
      }
    })
  }

  changePlayerAnimationState = (index, content) => {
    const newAnimationSwitchboard = Object.assign(
      {},
      this.state.playerAnimationSwitchboard,
      { [index]: { isAnimating: true, content } }
    )
    this.setState({ playerAnimationSwitchboard: newAnimationSwitchboard });
  }

  popPlayerAnimationState = (index) => {
    const persistContent = this.state.playerAnimationSwitchboard[index].content;
    const newAnimationSwitchboard = Object.assign(
      {},
      this.state.playerAnimationSwitchboard,
      { [index]: { isAnimating: false, content: persistContent } }
    )
    this.setState({ playerAnimationSwitchboard: newAnimationSwitchboard });
  }

  renderTable = () => {
    const {
      players,
      activePlayerIndex,
      dealerIndex,
      clearCards,
      phase,
      playerAnimationSwitchboard
    } = this.state;
    // Reverse Players Array for the sake of taking turns counter-clockwise.
    const reversedPlayers = players.reduce((result, player, index) => {

      const isActive = (index === activePlayerIndex);
      const hasDealerChip = (index === dealerIndex);


      result.unshift(
        <Player
          key={index}
          arrayIndex={index}
          isActive={isActive}
          hasDealerChip={hasDealerChip}
          player={player}
          clearCards={clearCards}
          phase={phase}
          playerAnimationSwitchboard={playerAnimationSwitchboard}
          endTransition={this.popPlayerAnimationState}
        />
      )
      return result
    }, []);
    return reversedPlayers.map(component => component);
  }

  renderPlayerActionButtons = () => {
    const { highBet, players, activePlayerIndex, phase, betInputValue } = this.state
    const min = calculateMinBet(highBet, players[activePlayerIndex].chips, players[activePlayerIndex].bet)
    const max = players[activePlayerIndex].chips + players[activePlayerIndex].bet
    return ((players[activePlayerIndex].robot) || (phase === 'showdown')) ? null : (
      <React.Fragment>
        <button className='bet-button' onClick={() => this.manageBetSubmit(betInputValue, min, max)}>
          {makeActionButtonText(highBet, betInputValue, players[activePlayerIndex])}
        </button>
        <button className='fold-button' onClick={() => this.managePlayerFold()}>
          Fold
        </button>
      </React.Fragment>
    )
  }

  renderTableCommunityCards = (purgeAnimation) => {
    return this.state.communityCards.map((card, index) => {
      let cardData = { ...card };
      if (purgeAnimation) {
        cardData.animationDelay = 0;
      }
      return (
        <Card key={index} cardData={cardData} />
      );
    });
  }

  renderPlayerShowdown = () => {
    return (
      <div className='showdown-div-wrapper'>
        <h5 className="showdown-div-title">
          Round Complete!
        </h5>
        <div className="showdown-div-messages">
          {makeShowdownMessages(this.state.showDownMessages)}
        </div>
        <h5 className="showdown-div-community-card-label">
          Community Cards
        </h5>
        <div className='showdown-div-community-cards'>
          {this.renderTableCommunityCards(true)}
        </div>
        <button className="showdown-nextRound-button" onClick={() => this.manageNextRound()}> Next Round </button>
        { this.renderBestHands()}
      </div>
    )
  }

  renderBestHands = () => {
    const { playerHierarchy } = this.state;

    return playerHierarchy.map(rankSnapshot => {
      const tie = Array.isArray(rankSnapshot);
      return tie ? this.renderHandSplit(rankSnapshot) : this.renderHandWinner(rankSnapshot);
    })
  }

  renderHandSplit = (rankSnapshot) => {
    return rankSnapshot.map(player => {
      return this.renderHandWinner(player);
    })
  }

  renderHandWinner = (player) => {
    const { name, bestHand, handRank } = player;
    const playerStateData = this.state.players.find(statePlayer => statePlayer.name === name);
    return (
      <div className="showdown-player" key={name}>
        <PlayerShowdown
          name={name}
          avatarURL={playerStateData.avatarURL}
          cards={playerStateData.cards}
          roundEndChips={playerStateData.roundEndChips}
          roundStartChips={playerStateData.roundStartChips}
        />
        <div className="showdown-player-besthand-div">
          <h5 className="showdown-player-besthand-heading">
            Best Hand
          </h5>
          <div className='showdown-player-besthand-cards' style={{ alignItems: 'center' }}>
            {
              bestHand.map((card, index) => {
                // Reset Animation Delay
                const cardData = { ...card, animationDelay: 0 }
                return <Card key={index} cardData={cardData} />
              })
            }
          </div>
        </div>
        <div className="showdown-handrank">
          {handRank}
        </div>
        {makeNetPlayerEarnings(playerStateData.roundEndChips, playerStateData.roundStartChips)}
      </div>
    )
  }

  renderGame = () => {
    const { highBet, players, activePlayerIndex, phase } = this.state;
    return (
      <div className='app-background'>
        <div className="title-text" style={{ maxWidth: "400px" }}></div>
        <div className="poker-table-div">
          <div className="title-logo">
          <img src={"./assets/logo.svg"}></img>
          <h3>No-Limit Texas Hold'em Poker</h3>
          <DropdownButton id="dropdown-basic-button" title="">
            <Dropdown.Item href="#"> <Link to="/dashboard">Return to Dashboard</Link></Dropdown.Item>
            <Dropdown.Item href="#"> <Link to="/login">Logout</Link></Dropdown.Item>
          </DropdownButton>
        </div>
          <img className="poker-table-image" src={"./assets/table.svg"} alt="Poker Table" />
          {this.renderTable()}
          <div className='community-hand-div' >
            {this.renderTableCommunityCards()}
          </div>
          <div className='pot-div'>
            <img style={{ height: 55, width: 55 }} src={'./assets/pot.svg'} alt="Pot Value" />
            <h5> {`${this.state.pot}`} </h5>
          </div>
        </div>
        { (this.state.phase === 'showdown') && this.renderPlayerShowdown()}
        <div className='game-bar' >
          <div className='game-buttons'>
            {this.renderPlayerActionButtons()}
          </div>
          <div className='slider'>
            {(!this.state.loading) && makeActionMenu(highBet, players, activePlayerIndex, phase, this.manageBetChange)}
          </div>
        </div>
      </div>
    )
  }

  render() {
    return (
      <div className="App">
        <div className='poker-table-wrapper'>
          {


            (this.state.loading) ? <SpinnerLoading /> :
              (this.state.winnerFound) ? <PlayerWin winner={this.state.winner} /> :
                this.renderGame()
          }

        </div>
      </div>
    );
  }
}

export default Game;
