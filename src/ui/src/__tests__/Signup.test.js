import React, {useRef, Component} from 'react';
import { Form, Button} from "react-bootstrap";
import renderer from 'react-test-renderer'

class testSignup extends Component {

    password = 'password'
    emailRef = useRef('test@test.com')
    passwordRef = useRef(this.password)
    passwordConfirmRef = useRef(this.password)


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
            <Form.Group id="password-confirm">
                <Form.Label>Password Confirmation</Form.Label>
                <Form.Control type="password" ref={passwordConfirmRef} required />
            </Form.Group>
            <Button className="w-100" type="submit">
                Sign Up
            </Button>
            </Form>
            </>
        )
    }
}

test('render user signup', () => {
    const component = renderer.create(
        <testSignup/>
    )
    let tree = component.toJSON()
    expect(tree).toMatchSnapshot()

})

test('match credentials', () => {
    expect(testSignup.emailRef).toBeUndefined()
    expect(testSignup.passwordRef).toBeUndefined()
})