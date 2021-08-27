# AskOptum Frontend

This is a work in progress...

- [Create React App](#create-react-app)
- [Scripts](#scripts)
- [Code Style](#code-style)
- [Formatting](#formatting)
- [Linting](#linting)


## Create React App

This project uses [Create React App](https://create-react-app.dev/). Check out [their docs](https://create-react-app.dev/docs/getting-started) for more information on the project.

## Scripts

You can run these scripts with either `yarn` or `npm`. The repository currently uses `npm`. 

- `start`: Start the application on port `3000`, with a proxy running to the `proxy` attribute from `package.json` for proxying API requests.
- `build`: Packages the application with webpack to the `./build` directory.
- `test`: Runs all tests with jest
- `eject`: Ejects CRA. There should be a team discussion and sufficient justification before electing to eject.
- `format`: Runs `prettier` on the code and writes results.
- `format:check`: Runs `prettier` and lists the changes it would make.
- `lint`: Runs `eslint` on the code and lists violations.
- `lint:fix`: Runs `eslint` on the code and auto-fixes any minor violations.




## Code Style

- Include one **single named** React functional component per-file.

    ```jsx
    // 👎

    // Button.tsx
    const Button = () => {}
    export default Button;

    // Uses Button.tsx
    import Button from 'components/Button';

    // 👍
    // Button.tsx
    export function Button() {}

    // Uses Button.tsx
    import {Button} from 'components';
    ```
- Prefer functional components over `const` or class-based components

    ```jsx
    // 👎
    class MyComponent {
        // ...
    }

    const MyComponent = () => {
        // ...
    }

    // 👍

    function MyComponent() {
        // ...
    }
    ```
- Prefer typescript where possible
- Look to reuse components from `@uitk/react` before implementing your own or using a different library
- React components should use PascalCase
- Export "public" components from the directory's `index.ts` file.
- Declare global types (such as API responses and other reusable types) in the `global` namespace `types/index.ts`
- Declare local types in the component file

    ```jsx
    // 👍

    interface IMyComponent {
        title: string;
    }
    export function MyComponent({title}) {}
    ```
- Destructure props in the function parameters, and assign default if option

    ```jsx   
    // 👍
    interface ISomeComponent {
        title: string;
        withHeader?: boolean;
    }
    export function SomeComponent({title, withHeader = false}) {}
    ```
- Use hooks to keep shared functionality/business logic portable to other components.
- Use absolute imports from the root `src` directory if you are importing components into another directory. Use relative imports if you are importing within a directory, or sub-directory. 

    ```jsx
    // pages/MainPage/MainPage.tsx

    // 👎
    import Button from '../../components/Button/Button';
    import colors from '../../styles/colors';

    // 👍
    import {Button} from 'components';
    import {colors} from 'styles';


    // components/Header/Header.tsx

    // 👍
    import {Button} from '../Button';

    ```

## Formatting

[`prettier`](https://prettier.io/) is used to format the codebase and keep it clean. There is a [vscode plugin](https://marketplace.visualstudio.com/items?itemName=esbenp.prettier-vscode) for prettier that you can configure to format your code on-save, or on-paste, such that it's always formatted before you check it in. 

## Linting

[`eslint`](https://eslint.org/) is used to lint our code. New rules/exceptions can be adopted as development continues. 