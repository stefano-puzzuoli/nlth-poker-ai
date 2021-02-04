import React, { useState } from "react"
import { Card, Button, Container, Alert } from "react-bootstrap"
import { useAuth } from "../contexts/AuthContext"
import { Link, useHistory } from "react-router-dom"
import Logo from './Logo';
import '../Poker.css';

export default function Dashboard() {
    const [error, setError] = useState("")
    const { currentUser, logout } = useAuth()
    const history = useHistory()

    async function handleLogout() {
        setError("")

        try {
            await logout()
            history.push("/login")
        } catch {
            setError("Failed to log out")
        }
    }

    async function playPoker() {
        setError("")

        try {
            history.push("/")
        } catch {
            setError("Failed to enter game")
        }
    }
    
    return (
        <>
            <Container
                className="d-flex flex-column align-items-center justify-content-center"
                style={{ minHeight: "100vh" }}
              >
                <div className="w-200 text-center">
                    <Logo/>
                </div>
                <div className="w-100" style={{ maxWidth: "400px" }}>
                    <Card>
                        <Card.Body>
                            <h2 className="text-center mb-4">Dashboard</h2>
                            {error && <Alert variant="danger">{error}</Alert>}
                    Welcome <strong> {currentUser.email} </strong>
                            <div className="w-100 text-center mt-2">
                                <Button className="w-100" onClick={playPoker}>
                                    Play Poker
                    </Button>
                            </div>
                        </Card.Body>
                    </Card>
                    <div className="w-100 text-center mt-2">
                        <Button variant="link" onClick={handleLogout}>
                            Log Out
                </Button>
                    </div>
                </div>
            </Container>
        </>
    )
}
