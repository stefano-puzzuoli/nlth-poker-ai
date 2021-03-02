import React, {Component, useRef} from 'react';
import { Card, Button, Alert} from "react-bootstrap";
import renderer from 'react-test-renderer'
import { Link } from 'react-router-dom'

class testForgotPassword extends Component {

    emailRef = useRef('test@test.com')


    render = () => {
        return (
            <>
            <Container
                className="d-flex align-items-center justify-content-center"
                style={{ minHeight: "100vh" }}
            >
                <div className="w-100" style={{ maxWidth: "400px" }}>
                <Card>
                    <Card.Body>
                    <h2 className="text-center mb-4">Password Reset</h2>
                    {<Alert variant="danger"></Alert>}
                    {<Alert variant="success"></Alert>}
                    <Form>
                        <Form.Group id="email">
                        <Form.Label>Email</Form.Label>
                        <Form.Control type="email" ref={emailRef} required />
                        </Form.Group>
                        <Button className="w-100" type="submit">
                        Reset Password
                    </Button>
                    </Form>
                    <div className="w-100 text-center mt-3">
                        <Link to="/login">Login</Link>
                    </div>
                    </Card.Body>
                </Card>
                <div className="w-100 text-center mt-2">
                    Need an account? <Link to="/signup">Sign Up</Link>
                </div>
                </div>
            </Container>
            </>
        )
    }
}

test('render forget password form', () => {
    const component = renderer.create(
        <testForgotPassword/>
    )
    let tree = component.toJSON()
    expect(tree).toMatchSnapshot()
})


