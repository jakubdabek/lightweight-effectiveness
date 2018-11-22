/*
 *  Copyright 2001-present Stephen Colebourne
 *
 *  Licensed under the Apache License, Version 2.0 (the "License");
 *  you may not use this file except in compliance with the License.
 *  You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 *  Unless required by applicable law or agreed to in writing, software
 *  distributed under the License is distributed on an "AS IS" BASIS,
 *  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 *  See the License for the specific language governing permissions and
 *  limitations under the License.
 */
package org.joda.beans.sample;

import java.util.Map;

import org.joda.beans.Bean;
import org.joda.beans.JodaBeanUtils;
import org.joda.beans.MetaBean;
import org.joda.beans.MetaProperty;
import org.joda.beans.gen.BeanDefinition;
import org.joda.beans.gen.PropertyDefinition;
import org.joda.beans.impl.direct.DirectMetaProperty;
import org.joda.beans.impl.direct.DirectMetaPropertyMap;

import com.google.common.collect.ImmutableMultiset;
import com.google.common.collect.Multiset;

/**
 * Mock immutable person JavaBean, used for testing.
 * 
 * @author Stephen Colebourne
 */
@BeanDefinition(hierarchy = "immutable", cacheHashCode = true)
public final class ImmSubSubPersonFinal extends ImmSubPersonNonFinal {

    @PropertyDefinition
    private final ImmutableMultiset<String> codeCounts;

    //------------------------- AUTOGENERATED START -------------------------
    /**
     * The meta-bean for {@code ImmSubSubPersonFinal}.
     * @return the meta-bean, not null
     */
    public static ImmSubSubPersonFinal.Meta meta() {
        return ImmSubSubPersonFinal.Meta.INSTANCE;
    }

    static {
        MetaBean.register(ImmSubSubPersonFinal.Meta.INSTANCE);
    }

    /**
     * The cached hash code, using the racy single-check idiom.
     */
    private transient int cacheHashCode;

    /**
     * Returns a builder used to create an instance of the bean.
     * @return the builder, not null
     */
    public static ImmSubSubPersonFinal.Builder builder() {
        return new ImmSubSubPersonFinal.Builder();
    }

    /**
     * Restricted constructor.
     * @param builder  the builder to copy from, not null
     */
    private ImmSubSubPersonFinal(ImmSubSubPersonFinal.Builder builder) {
        super(builder);
        this.codeCounts = (builder.codeCounts != null ? ImmutableMultiset.copyOf(builder.codeCounts) : null);
    }

    @Override
    public ImmSubSubPersonFinal.Meta metaBean() {
        return ImmSubSubPersonFinal.Meta.INSTANCE;
    }

    //-----------------------------------------------------------------------
    /**
     * Gets the codeCounts.
     * @return the value of the property
     */
    public ImmutableMultiset<String> getCodeCounts() {
        return codeCounts;
    }

    //-----------------------------------------------------------------------
    /**
     * Returns a builder that allows this bean to be mutated.
     * @return the mutable builder, not null
     */
    @Override
    public Builder toBuilder() {
        return new Builder(this);
    }

    @Override
    public boolean equals(Object obj) {
        if (obj == this) {
            return true;
        }
        if (obj != null && obj.getClass() == this.getClass()) {
            ImmSubSubPersonFinal other = (ImmSubSubPersonFinal) obj;
            return JodaBeanUtils.equal(codeCounts, other.codeCounts) &&
                    super.equals(obj);
        }
        return false;
    }

    @Override
    public int hashCode() {
        int hash = cacheHashCode;
        if (hash == 0) {
            hash = 7;
            hash = hash * 31 + JodaBeanUtils.hashCode(codeCounts);
            hash = hash ^ super.hashCode();
            cacheHashCode = hash;
        }
        return hash;
    }

    @Override
    public String toString() {
        StringBuilder buf = new StringBuilder(64);
        buf.append("ImmSubSubPersonFinal{");
        int len = buf.length();
        toString(buf);
        if (buf.length() > len) {
            buf.setLength(buf.length() - 2);
        }
        buf.append('}');
        return buf.toString();
    }

    @Override
    protected void toString(StringBuilder buf) {
        super.toString(buf);
        buf.append("codeCounts").append('=').append(JodaBeanUtils.toString(codeCounts)).append(',').append(' ');
    }

    //-----------------------------------------------------------------------
    /**
     * The meta-bean for {@code ImmSubSubPersonFinal}.
     */
    public static final class Meta extends ImmSubPersonNonFinal.Meta {
        /**
         * The singleton instance of the meta-bean.
         */
        static final Meta INSTANCE = new Meta();

        /**
         * The meta-property for the {@code codeCounts} property.
         */
        @SuppressWarnings({"unchecked", "rawtypes" })
        private final MetaProperty<ImmutableMultiset<String>> codeCounts = DirectMetaProperty.ofImmutable(
                this, "codeCounts", ImmSubSubPersonFinal.class, (Class) ImmutableMultiset.class);
        /**
         * The meta-properties.
         */
        private final Map<String, MetaProperty<?>> metaPropertyMap$ = new DirectMetaPropertyMap(
                this, (DirectMetaPropertyMap) super.metaPropertyMap(),
                "codeCounts");

        /**
         * Restricted constructor.
         */
        private Meta() {
        }

        @Override
        protected MetaProperty<?> metaPropertyGet(String propertyName) {
            switch (propertyName.hashCode()) {
                case -1383758447:  // codeCounts
                    return codeCounts;
            }
            return super.metaPropertyGet(propertyName);
        }

        @Override
        public ImmSubSubPersonFinal.Builder builder() {
            return new ImmSubSubPersonFinal.Builder();
        }

        @Override
        public Class<? extends ImmSubSubPersonFinal> beanType() {
            return ImmSubSubPersonFinal.class;
        }

        @Override
        public Map<String, MetaProperty<?>> metaPropertyMap() {
            return metaPropertyMap$;
        }

        //-----------------------------------------------------------------------
        /**
         * The meta-property for the {@code codeCounts} property.
         * @return the meta-property, not null
         */
        public MetaProperty<ImmutableMultiset<String>> codeCounts() {
            return codeCounts;
        }

        //-----------------------------------------------------------------------
        @Override
        protected Object propertyGet(Bean bean, String propertyName, boolean quiet) {
            switch (propertyName.hashCode()) {
                case -1383758447:  // codeCounts
                    return ((ImmSubSubPersonFinal) bean).getCodeCounts();
            }
            return super.propertyGet(bean, propertyName, quiet);
        }

        @Override
        protected void propertySet(Bean bean, String propertyName, Object newValue, boolean quiet) {
            metaProperty(propertyName);
            if (quiet) {
                return;
            }
            throw new UnsupportedOperationException("Property cannot be written: " + propertyName);
        }

    }

    //-----------------------------------------------------------------------
    /**
     * The bean-builder for {@code ImmSubSubPersonFinal}.
     */
    public static final class Builder extends ImmSubPersonNonFinal.Builder {

        private Multiset<String> codeCounts;

        /**
         * Restricted constructor.
         */
        private Builder() {
        }

        /**
         * Restricted copy constructor.
         * @param beanToCopy  the bean to copy from, not null
         */
        private Builder(ImmSubSubPersonFinal beanToCopy) {
            super(beanToCopy);
            this.codeCounts = beanToCopy.getCodeCounts();
        }

        //-----------------------------------------------------------------------
        @Override
        public Object get(String propertyName) {
            switch (propertyName.hashCode()) {
                case -1383758447:  // codeCounts
                    return codeCounts;
                default:
                    return super.get(propertyName);
            }
        }

        @SuppressWarnings("unchecked")
        @Override
        public Builder set(String propertyName, Object newValue) {
            switch (propertyName.hashCode()) {
                case -1383758447:  // codeCounts
                    this.codeCounts = (Multiset<String>) newValue;
                    break;
                default:
                    super.set(propertyName, newValue);
                    break;
            }
            return this;
        }

        @Override
        public Builder set(MetaProperty<?> property, Object value) {
            super.set(property, value);
            return this;
        }

        @Override
        public ImmSubSubPersonFinal build() {
            return new ImmSubSubPersonFinal(this);
        }

        //-----------------------------------------------------------------------
        /**
         * Sets the codeCounts.
         * @param codeCounts  the new value
         * @return this, for chaining, not null
         */
        public Builder codeCounts(Multiset<String> codeCounts) {
            this.codeCounts = codeCounts;
            return this;
        }

        //-----------------------------------------------------------------------
        @Override
        public String toString() {
            StringBuilder buf = new StringBuilder(64);
            buf.append("ImmSubSubPersonFinal.Builder{");
            buf.append("codeCounts").append('=').append(JodaBeanUtils.toString(codeCounts));
            buf.append('}');
            return buf.toString();
        }

    }

    //-------------------------- AUTOGENERATED END --------------------------
}
