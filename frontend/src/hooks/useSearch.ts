import {useQuery, useQueryClient} from 'react-query';
import {apiClient} from 'helpers';

const searchQueryKey = 'search';
const defaultResponse: ISearchResponse = {
  domains: [],
  query: '',
  results: [],
};

export function useSearch(query?: string | null) {
  const queryKey = `${searchQueryKey}#${query}`;
  const queryClient = useQueryClient();

  const {
    data,
    refetch,
    isLoading: isLoadingAtAll,
    isFetching,
    isError,
  } = useQuery<ISearchResponse, Error>(
    queryKey,
    async () => {
      const {body, headers} = await apiClient(`search?q=${query}`, {
        method: 'GET',
      });

      return {
        ...body,
        traceId: headers['trace-id'],
      };
    },
    {
      enabled: !!query,
      refetchOnWindowFocus: false,
      onError: (_) => {
        queryClient.setQueryData(queryKey, defaultResponse);
      },
    },
  );

  return {
    data,
    refetch,
    isLoading: isLoadingAtAll || isFetching,
    isError,
  };
}
