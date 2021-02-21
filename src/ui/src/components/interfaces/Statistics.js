import React, { useEffect, useState } from "react"
import { Button, Card, Container, Alert } from "react-bootstrap"
import { useAuth } from "../../contexts/AuthContext"
import { useHistory } from "react-router-dom"
import firebaseDb from "../../firebase"
import Logo from '../helpers/Logo';
import '../../Game.css';

/**
 * UserStatistics component to allow users view
 * their individual game statistics.
 */
function UserStatistics({ userStatistics }) {

    const history = useHistory()

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
        <>
            <div>
                <div> Beginner Games Played : {userStatistics.num_beginner_games}</div>
                <div> Beginner Games Won : {userStatistics.num_beginner_wins}</div>
                <div> Intermediate Games Played : {userStatistics.num_intermediate_games}</div>
                <div> Intermediate Games Won : {userStatistics.num_intermediate_wins}</div>
                <div> Expert Games Played : {userStatistics.num_expert_games}</div>
                <div> Expert Games Won : {userStatistics.num_expert_wins}</div>
                <div> Ultimate Poker Pro Games Played : {userStatistics.num_ultimate_games}</div>
                <div> Ultimate Poker Pro Games Won : {userStatistics.num_ultimate_wins}</div>
                <div> Total Games Played : {userStatistics.num_beginner_games + userStatistics.num_intermediate_games + userStatistics.num_expert_games + userStatistics.num_ultimate_games}</div>
                <div> Total Games Won : {userStatistics.num_beginner_wins + userStatistics.num_intermediate_wins + userStatistics.num_expert_wins + userStatistics.num_ultimate_wins}</div>

            </div>
            <Button className="w-100 mt-3" onClick={handleReturnToDashboard}>
                Return to Dashboard
            </Button>
        </>
    );
}

function GuestUserStatistics({ userStatistics }) {
    const history = useHistory()

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
        <>
            <div>
                <div>No Statistics Recorded for Guest Users</div>
            </div>
            <Button className="w-100 mt-3" onClick={handleReturnToDashboard}>
                Return to Dashboard
            </Button>
        </>
    );
}



export default function Statistics(props) {
    const { currentUser } = useAuth()
    const [loading, setLoading] = useState(true);
    const [userStats, setUserStats] = useState(new Object());
    var userStatistics = new Object();

    useEffect(() => {
        setUserStatistics()
    });

    async function setUserStatistics() {

        var countValues = 0;
        // If email is guest email show message saying that as a guest player nos stats are recorded
        firebaseDb.database().ref().child(currentUser.uid).once("value").then(function (snapshot) {
            console.log("snapshot");
            console.log(snapshot);
            snapshot.forEach(function (childSnapshot) {
                var key = childSnapshot.key;
                var childData = childSnapshot.val();
                userStatistics[key] = childData;
                countValues += 1;

            });

            if (countValues == 0) {
                userStatistics = {
                    "num_beginner_games": 0, "num_beginner_wins": 0,
                    "num_intermediate_games": 0, "num_intermediate_wins": 0,
                    "num_expert_games": 0, "num_expert_wins": 0,
                    "num_ultimate_games": 0, "num_ultimate_wins": 0,
                }
            }
            setUserStats(userStatistics)

            if (countValues == 8) {
                setLoading(false);
            }
        }
        )
    }

    return (
        <>

            <Container
                className="d-flex flex-column align-items-center justify-content-center"
                style={{ minHeight: "100vh" }}
            >
                <div className="w-200 text-center">
                    <Logo />
                </div>
                <div className="w-100" style={{ maxWidth: "400px" }}>
                    <Card>
                        <Card.Body>
                            <h2 className="text-center mb-4">Personal Statistics</h2>

                            {
                                (currentUser.email == "guest@guest.com") ? <GuestUserStatistics /> :
                                    (loading) ? "Loading..." : <UserStatistics userStatistics={userStats} />
                            }

                        </Card.Body>

                    </Card>
                </div>
            </Container>
        </>
    )
}


