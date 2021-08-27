import styled from 'styled-components';
import {Text} from '@uitk/react';
import {theme} from 'styles';
import {FeedbackButton} from '../Button/FeedbackButton';
import {Feedback} from 'types';

const Wrapper = styled.div`
  display: flex;
  flex-direction: row;
  justify-content: flex-end;
  align-items: center;
  width: 100%;
  border-bottom: none;
  position: relative;
  padding-top: ${theme.spacingXS};
  padding-bottom: ${theme.spacingXS};
  margin-top: ${theme.spacingM};
  margin-bottom: ${theme.spacingXL};
  margin: 0;

  &:after {
    content: '';
    background: ${theme.colorBackgroundAccent};
    display: block;
    height: ${theme.spacingXXS};
    width: 100%;
    position: absolute;
    bottom: 0;
  }
`;

const AnswerText = styled(Text).attrs(() => ({as: 'p'}))`
  color: ${theme.colorTextFormHelp};
  font-size: ${theme.fontSizeFormHelp};
  font-weight: ${theme.fontWeightLight};
  line-height: 1.5;
  padding-right: ${theme.spacingXS};
  padding-left: ${theme.spacingXS};
  margin: 0;
`;

const Item = styled.div`
  display: inline-flex;
  align-items: center;
  padding-left: ${theme.spacingXS};
  padding-right: ${theme.spacingXS};
`;

interface IAnswerSkill {
  onPress: (feedback: Feedback) => void;
}
export function AnswerSkill({onPress}: IAnswerSkill) {
  return (
    <Wrapper>
      <Item>
        <AnswerText>Is this answer helpful?</AnswerText>
        <FeedbackButton onPress={onPress} />
      </Item>
    </Wrapper>
  );
}
