import ReactMarkdown from 'react-markdown';
import gfm from 'remark-gfm';
import {createGlobalStyle} from 'styled-components';
import {theme} from 'styles';
import {Domains} from 'types';
import {Button} from 'components';
import {useState, useCallback, MouseEvent} from 'react';
import './Markdown.scss';
import {ArrowUp, ArrowDown} from '@uitk/react-icons';

interface IMarkdown {
  content?: string;
  domain?: Domains;
  onClick?: (e: MouseEvent<HTMLAnchorElement>) => void;
}

const className = 'markdown';

// Used to style markdown elements differently by domain/skill
const MarkdownStyle = createGlobalStyle`
  .${className} {
    & > h1,h2,h3,h4,h5,h6 {
      margin-top: ${theme.spacingXS};
      margin-bottom: ${theme.spacingXS};
    }
    & > table {
      margin-top: ${theme.spacingSM};
      margin-bottom: ${theme.spacingLG};
      td {
        text-align: left;
        padding-left: ${theme.spacingLG};
        padding-right: ${theme.spacingLG};
        background-color: ${theme.colorBackgroundDropdown};
      },
      th {
        background-color: ${theme.colorBackgroundAccent};
      }
    }
  }
`;

export function Markdown({
  content,
  domain = Domains.unknown,
  onClick = () => {},
}: IMarkdown) {
  const markdownComponents = {
    a: ({...props}) => <Button.Link onClick={onClick} {...props} />,
  };
  const [isOpen, setIsOpen] = useState(false);

  const handleToggle = useCallback(
    (e: MouseEvent<HTMLAnchorElement>) => {
      e.preventDefault();
      setIsOpen((wasOpened) => !wasOpened);
    },
    [setIsOpen],
  );

  return (
    <>
      <MarkdownStyle />
      {content && content?.length < 500 && (
        <ReactMarkdown
          components={markdownComponents}
          remarkPlugins={[gfm]}
          className={`${className} ${domain}`}
          linkTarget="_blank">
          {content ?? ''}
        </ReactMarkdown>
      )}

      {content && content?.length >= 500 && (
        <div className="mark-down-container">
          <div className={`${isOpen}`}>
            <ReactMarkdown
              components={markdownComponents}
              remarkPlugins={[gfm]}
              className={`${className} ${domain}`}
              linkTarget="_blank">
              {content ?? ''}
            </ReactMarkdown>
          </div>
          {isOpen ? (
            <a className="link" onClick={handleToggle} href="/#">
              See Less <ArrowUp />
            </a>
          ) : (
            <a className="link" onClick={handleToggle} href="/#">
              See More <ArrowDown />
            </a>
          )}
        </div>
      )}
    </>
  );
}
