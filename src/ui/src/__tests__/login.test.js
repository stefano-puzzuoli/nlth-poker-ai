import React, {useRef, Component} from 'react';
import { Form, Button} from "react-bootstrap";
import renderer from 'react-test-renderer'

class testLogin extends Component {

    emailRef = useRef('test@test.com')
    passwordRef = useRef('password')

    render = () => {
        return (
            <>
                <Form>
                <Form.Group id="email">
                    <Form.Label>Email</Form.Label>
                    <Form.Control type="email" ref={emailRef} required />
                </Form.Group>
                <Form.Group id="password">
                    <Form.Label>Password</Form.Label>
                    <Form.Control type="password" ref={passwordRef} required />
                </Form.Group>
                <Button className="w-100" type="submit">
                    Log In
                </Button>
                </Form>
            </>
        )
    }
}
test('render user login', () => {
    const component = renderer.create(
        <testLogin/>
    )
    let tree = component.toJSON()
    expect(tree).toMatchSnapshot()

})