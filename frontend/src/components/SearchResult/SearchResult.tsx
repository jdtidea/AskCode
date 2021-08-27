import './SearchResult.scss';
import {useCallback, useMemo, MouseEvent} from 'react';
import {AnswerSkill, Markdown} from 'components';
import styled from 'styled-components';
import {Panel} from '@uitk/react';
import DOMPurify from 'dompurify';
import {useAnalytics, TrackingEventsEnum} from 'analytics';
import {useUser} from 'auth';
import {Feedback} from 'types';
import {config} from 'config';
import {theme, colors} from 'styles';

const Container = styled.div.attrs(() => ({
  className: 'col-12',
}))`
  display: flex;
  flex-direction: column;
  text-align: left;
  align-self: center;
  width: 100%;
`;

const TitleText = styled.div`
  display: flex;
  flex-direction: row;
  justify-content: flex-start;
  align-items: center;
`;

const Wrapper = styled.div`
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
  width: 100%;
  border-bottom: none;
  position: relative;
  padding-top: ${theme.spacingXL};
  padding-bottom: ${theme.spacingXS};
  margin-top: ${theme.spacingM};
  margin-bottom: ${theme.spacingXL};
  margin: 0;

  &:after {
    content: '';
    background: ${colors.gradientOrange100};
    display: block;
    height: ${theme.spacingXXS};
    width: 102%;
    position: absolute;
    bottom: 0;
    left: -1%;
    margin-bottom: 15px;
  }
`;

export interface ISearchResult extends ISearchResultResponse {
  query: string;
  traceId?: string;
  index: any;
}

export function SearchResult({
  index,
  title,
  url,
  skill = 'Optum',
  domain,
  variant,
  content,
  query,
  traceId,
}: ISearchResult) {
  const trackFeedback = useAnalytics(TrackingEventsEnum.SEARCH_FEEDBACK);
  const trackClick = useAnalytics(TrackingEventsEnum.CONTENT_CLICK);
  const {userId} = useUser();

  const handleClick = useCallback(
    (e: MouseEvent<HTMLAnchorElement>) => {
      trackClick({
        query,
        domain,
        skill,
        userId,
        traceId,
        threshold: config.domainThreshold,
        href: e.currentTarget.href,
      });
    },
    [domain, query, skill, trackClick, userId, traceId],
  );

  const Title = useMemo(() => {
    return url ? (
      <TitleText>
        <h4 className="header-with-link">
          <a
            href={url}
            className="header-link"
            target="_blank"
            rel="noreferrer"
            onClick={handleClick}>
            {title}
          </a>
        </h4>
      </TitleText>
    ) : (
      <TitleText>
        <h4>{title}</h4>
      </TitleText>
    );
  }, [title, url, handleClick]);
  const handleFeedback = useCallback(
    (feedback: Feedback) => {
      trackFeedback({
        query,
        domain,
        skill,
        feedback,
        userId,
        traceId,
        threshold: config.domainThreshold,
      });
    },
    [domain, query, skill, trackFeedback, userId, traceId],
  );

  const renderItemContent = useCallback(
    (variant: TSearchContentVariant, content: string) => {
      switch (variant) {
        case 'md':
          return (
            <Markdown content={content} domain={domain} onClick={handleClick} />
          );
        case 'html':
          return DOMPurify.sanitize(content);
        default:
          return content;
      }
    },
    [domain, handleClick],
  );

  const renderItems = useCallback(() => {
    return <Panel.Group>{renderItemContent(variant, content)}</Panel.Group>;
  }, [variant, content, renderItemContent]);

  if (index === 0) {
    return (
      <div className="row best-answer">
        <Container>
          {Title}
          {renderItems()}
          <AnswerSkill onPress={handleFeedback} />
        </Container>
      </div>
    );
  } else if (index === 1) {
    return (
      <div>
        <div className="row best-answer">
          <Container>
            {Title}
            {renderItems()}
            <AnswerSkill onPress={handleFeedback} />
          </Container>
        </div>
        <Wrapper></Wrapper>
      </div>
    );
  } else {
    return (
      <div className="row">
        <Container>
          {Title}
          {renderItems()}
          <AnswerSkill onPress={handleFeedback} />
        </Container>
      </div>
    );
  }
}
