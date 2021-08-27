// TODO: replace with react-toastify
import {Tooltip} from '@uitk/react';
import {useEffect, useState} from 'react';
import styled from 'styled-components';
import {theme} from 'styles';

const Wrapper = styled.div<{visible: boolean}>`
  display: ${(p) => (p.visible ? 'block' : 'none')};
  height: 0;
  width: 0;
  // Tooltip
  & > span > div {
    padding: ${theme.spacingSM};
    border-radius: ${theme.spacingSM};
    text-align: center;
    margin-bottom: ${theme.spacingLG};
  }
  // Arrow
  & > span > div > div {
    display: none;
  }
`;

interface IToast {
  text?: JSX.Element;
  delayMS?: number;
}

export function Toast({
  text = (
    <span>
      Thank you for your feedback!
      <br />
      This helps us improve.
    </span>
  ),
  delayMS = 5000,
}: IToast) {
  const [visible, setVisible] = useState(true);

  useEffect(() => {
    setTimeout(() => {
      setVisible(false);
    }, delayMS);
  }, [delayMS]);

  return visible ? (
    <Wrapper visible={visible}>
      <Tooltip content={text} visible={visible}>
        <></>
      </Tooltip>
    </Wrapper>
  ) : null;
}
