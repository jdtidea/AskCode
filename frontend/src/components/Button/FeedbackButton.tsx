import {useCallback, useState} from 'react';
import styled from 'styled-components';
import {theme} from 'styles';
import {darken} from 'polished';
import {Button} from '@uitk/react';
import {ThumbsUp as Icon} from '@uitk/react-icons';
import {Toast} from '../Toast';
import {Feedback} from 'types';

interface IFeedbackButton {
  onPress: (feedback: Feedback) => void;
}

const Wrapper = styled.div`
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
`;

const StyledButton = styled(Button).attrs({
  variant: 'ghost-alternative',
})<{selected: boolean}>`
  display: flex;
  border-radius: ${theme.spacingXXS};
  font-size: ${theme.spacingSM};
  padding: ${theme.spacingXXS};
  margin-left: ${theme.spacingXXS};
  margin-right: ${theme.spacingXXS};
  min-height: ${theme.spacingXXS};
  ${(p) =>
    p.selected
      ? `
      &:disabled,
      &:disabled:hover,
      &:disabled:active,
      &:disabled:focus {
        color: ${theme.colorTextBrandPrimary};
        background: ${darken(0.05, theme.colorBackgroundAltButtonInteractive)};
      }
  `
      : null}
  &:hover,
  &:focus {
    box-shadow: none;
  }
`;

const ThumbsUp = styled(Icon)`
  height: ${theme.spacingSM};
  width: ${theme.spacingSM};
`;
const ThumbsDown = styled(ThumbsUp)`
  transform: scaleY(-1);
`;

export function FeedbackButton({onPress}: IFeedbackButton) {
  const [isPressed, setIsPressed] = useState<Feedback | undefined>();
  const handlePress = useCallback(
    (feedback: Feedback) => {
      setIsPressed(feedback);
      onPress(feedback);
    },
    [onPress],
  );

  return (
    <Wrapper>
      <StyledButton
        selected={isPressed === Feedback.yes}
        onClick={() => {
          handlePress(Feedback.yes);
        }}
        onSubmit={() => {
          handlePress(Feedback.yes);
        }}
        isDisabled={!!isPressed}
        icon={<ThumbsUp />}>
        {Feedback.yes}
      </StyledButton>
      {!!isPressed ? <Toast /> : null}
      <StyledButton
        selected={isPressed === Feedback.no}
        onClick={() => {
          handlePress(Feedback.no);
        }}
        onSubmit={() => {
          handlePress(Feedback.no);
        }}
        isDisabled={!!isPressed}
        icon={<ThumbsDown />}>
        {Feedback.no}
      </StyledButton>
    </Wrapper>
  );
}
