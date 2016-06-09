package com.newicom.chesskid;

import org.apache.commons.io.IOUtils;
import org.mockserver.client.server.MockServerClient;
import org.mockserver.model.Body;
import org.mockserver.model.Header;
import org.mockserver.model.Parameter;
import org.mockserver.model.StringBody;

import java.io.IOException;
import java.io.InputStream;

import static org.mockserver.model.HttpRequest.request;
import static org.mockserver.model.HttpResponse.response;

public class MockConfigurator {

    public static final int PAGES_NR = 23;

    public static void main(String[] args) throws IOException {

        MockServerClient mock = new MockServerClient("127.0.0.1", 1080);
        mock.reset();

        setupLastPage(mock);

        for (int i = 1; i < PAGES_NR; i++) {
            setupPage(mock, i);
        }

    }

    private static void setupLastPage(MockServerClient mock) throws IOException {
        mock
            .when(
                    request()
                            .withMethod("GET")
                            .withPath("/home/game_archive.html")
                            .withQueryStringParameters(
                                    new Parameter("member", "Pawel"),
                                    new Parameter("show", "live"),
                                    new Parameter("page", "last")
                            )
            )
            .respond(
                    response()
                            .withBody(readFile("last.html"))
                            .withHeaders(
                                    new Header("Content-Type", "text/html; charset=utf-8")
                            )
            );
    }

    private static void setupPage(MockServerClient mock, int pageNr) throws IOException {
        mock
            .when(
                    request()
                            .withMethod("GET")
                            .withPath("/home/game_archive.html")
                            .withQueryStringParameters(
                                    new Parameter("member", "Pawel"),
                                    new Parameter("show", "live"),
                                    new Parameter("page", String.valueOf(pageNr))
                            )
            )
            .respond(
                    response()
                            .withBody(readFile(pageNr + ".html"))
                            .withHeaders(
                                    new Header("Content-Type", "text/html; charset=utf-8")
                            )
            );
    }

    private static Body readFile(String fileName) throws IOException {
        try {
            InputStream stream = MockConfigurator.class.getClassLoader().getResourceAsStream(fileName);
            return new StringBody(IOUtils.toString(stream));
        } catch (Exception ex) {
            return readFile("last.html");
        }
    }
}
