import React, { useEffect } from "react"
import { Button, Card, Container } from "react-bootstrap"
import { useHistory, useLocation } from "react-router-dom"
import { useAuth } from "../../contexts/AuthContext"
import firebaseDb from "../../firebase"

export default function PlayerWin(props) {
    const { currentUser } = useAuth()
    const history = useHistory()

    const search = useLocation().search;
    const difficulty = new URLSearchParams(search).get('difficulty');

    
    useEffect(() => {
        recordUserStatistics()
    });

    async function recordUserStatistics(e) {
        var userStatistics = new Object();
        firebaseDb.database().ref().child(currentUser.uid).once("value").then(function (snapshot) {
            var countValues = 0;
            snapshot.forEach(function (childSnapshot) {
                var key = childSnapshot.key;
                var childData = childSnapshot.val();
                userStatistics[key] = childData;
                countValues += 1;
            });
            if (countValues == 0) {
                firebaseDb.database().ref().child(currentUser.uid).set({
                    "num_beginner_games": 0, "num_beginner_wins": 0,
                    "num_intermediate_games": 0, "num_intermediate_wins": 0,
                    "num_expert_games": 0, "num_expert_wins": 0,
                    "num_ultimate_games": 0, "num_ultimate_wins": 0,
                })
                userStatistics = {
                    "num_beginner_games": 0, "num_beginner_wins": 0,
                    "num_intermediate_games": 0, "num_intermediate_wins": 0,
                    "num_expert_games": 0, "num_expert_wins": 0,
                    "num_ultimate_games": 0, "num_ultimate_wins": 0,
                }
            }
        }
    }

    async function handleReturnToDashboard(e) {
        e.preventDefault()
        console.log("Returning to dashboard...")
        try {
            history.push("/dashboard")
        } catch {
            console.log("Error returning to dashboard. Please try again.")
        }
    }

    return (
        <Container
            className="d-flex flex-column align-items-center justify-content-center"
            style={{ minHeight: "100vh" }}
        >
            <div className="w-100" style={{ maxWidth: "400px" }}>
                <Card>
                    <Card.Body>
                        <div className="w-200 text-center">
                            <img className="logo mr-2" src="/assets/win-trophy.png" />
                        </div>
                        <div className="w-100 m-100">
                            <h2>
                                {props.winner.name} Wins!
                            </h2>
                        </div>
                        <Button className="w-100 mt-3" onClick={handleReturnToDashboard}>
                            Return to Dashboard
                    </Button>
                    </Card.Body>
                </Card>
            </div>
        </Container>
    )
}