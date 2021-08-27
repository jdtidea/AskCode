import './Description.scss';
import styled from 'styled-components';
import {theme} from 'styles';
import {MemberLinkUserProfile} from 'components';

const Wrapper = styled.div`
  flex-direction: column;
  align-items: flex-start;
  margin-left: 30px;
  & > p {
    text-align: initial;
  }
`;

const Header = styled.h2`
  margin: 0;
  margin-top: ${theme.spacingM};
`;

export function Description() {
  return (
    <Wrapper>
      <Header>Link your healthcare information</Header>
      <p>
        <b>Why is it helpful to provide this information?</b>
      </p>
      <p>
        Linking your information enables AskOptum to give you personalized
        answers as a UnitedHealthcare member and employee all in the same place.
      </p>
      <p>You can unlink your information at any time.</p>

      <MemberLinkUserProfile />
    </Wrapper>
  );
}
