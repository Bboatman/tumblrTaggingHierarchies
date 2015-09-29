package edu.macalester.wikibrainmap;

import org.wikibrain.Loader;
import org.wikibrain.conf.ConfigurationException;
import org.wikibrain.core.WikiBrainException;
import org.wikibrain.core.cmd.Env;
import org.wikibrain.core.cmd.EnvBuilder;
import org.wikibrain.core.dao.DaoException;
import org.wikibrain.core.lang.Language;
import org.wikibrain.matrix.DenseMatrix;
import org.wikibrain.sr.SRBuilder;
import org.wikibrain.sr.SRMetric;
import org.wikibrain.sr.vector.DenseVectorSRMetric;

import java.io.IOException;
import java.sql.SQLException;

/**
 * @author Shilad Sen
 */
public class Test {
    public static void buildModel() throws Exception {
        Loader.main(new String[] {"-l", "simple", "-c", "wb-map.conf"});
        SRBuilder.main(new String[]{"-m", "word2vec-wbmap", "-g", "wordsim353.txt"});

    }
    public static void main(String args[]) throws Exception {
        // Only do this once
        buildModel();

        Env env = EnvBuilder.envFromArgs(new String[]{"-c", "wb-map.conf"});
        DenseVectorSRMetric w2v = (DenseVectorSRMetric) env.getConfigurator().get(
                SRMetric.class, "word2vec-wbmap", "language", Language.SIMPLE.getLangCode());
        DenseMatrix matrix = w2v.getGenerator().getFeatureMatrix();
    }
}
