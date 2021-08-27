import styled from 'styled-components';
import {Button} from '@uitk/react';
import {Search} from '@uitk/react-icons';
import {theme} from 'styles';

const StyledButton = styled(Button)`
  width: 100%;
  justify-content: center;
  padding: ${theme.spacingSM};
`;

export function SearchButton({
  type = 'submit',
  ...rest
}: {
  type?: 'button' | 'submit' | 'reset' | undefined;
}) {
  return (
    <StyledButton type={type} icon={<Search />} {...rest}>
      Ask Optum
    </StyledButton>
  );
}
