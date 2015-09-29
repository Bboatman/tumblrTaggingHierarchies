package edu.macalester.wikibrainmap;

import org.wikibrain.Loader;
import org.wikibrain.conf.ConfigurationException;
import org.wikibrain.core.dao.DaoException;

import java.io.IOException;
import java.sql.SQLException;

/**
 * @author Shilad Sen
 */
public class Test {
    public static void main(String args[]) throws InterruptedException, IOException, DaoException, SQLException, ConfigurationException, ClassNotFoundException {
        Loader.main(new String[] {"-l", "simple"});
    }
}
