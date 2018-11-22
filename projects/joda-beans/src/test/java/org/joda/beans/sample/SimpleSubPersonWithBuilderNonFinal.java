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
import org.joda.beans.Property;
import org.joda.beans.gen.BeanDefinition;
import org.joda.beans.gen.PropertyDefinition;
import org.joda.beans.impl.direct.DirectMetaProperty;
import org.joda.beans.impl.direct.DirectMetaPropertyMap;

/**
 * Mock person JavaBean, used for testing.
 * 
 * @author Stephen Colebourne
 */
@BeanDefinition(builderScope = "public")
public class SimpleSubPersonWithBuilderNonFinal extends SimplePersonWithBuilderNonFinal {

    /** The middle name. */
    @PropertyDefinition
    private String middleName;

    //------------------------- AUTOGENERATED START -------------------------
    /**
     * The meta-bean for {@code SimpleSubPersonWithBuilderNonFinal}.
     * @return the meta-bean, not null
     */
    public static SimpleSubPersonWithBuilderNonFinal.Meta meta() {
        return SimpleSubPersonWithBuilderNonFinal.Meta.INSTANCE;
    }

    static {
        MetaBean.register(SimpleSubPersonWithBuilderNonFinal.Meta.INSTANCE);
    }

    /**
     * Returns a builder used to create an instance of the bean.
     * @return the builder, not null
     */
    public static SimpleSubPersonWithBuilderNonFinal.Builder builder() {
        return new SimpleSubPersonWithBuilderNonFinal.Builder();
    }

    /**
     * Restricted constructor.
     * @param builder  the builder to copy from, not null
     */
    protected SimpleSubPersonWithBuilderNonFinal(SimpleSubPersonWithBuilderNonFinal.Builder builder) {
        super(builder);
        this.middleName = builder.middleName;
    }

    @Override
    public SimpleSubPersonWithBuilderNonFinal.Meta metaBean() {
        return SimpleSubPersonWithBuilderNonFinal.Meta.INSTANCE;
    }

    //-----------------------------------------------------------------------
    /**
     * Gets the middle name.
     * @return the value of the property
     */
    public String getMiddleName() {
        return middleName;
    }

    /**
     * Sets the middle name.
     * @param middleName  the new value of the property
     */
    public void setMiddleName(String middleName) {
        this.middleName = middleName;
    }

    /**
     * Gets the the {@code middleName} property.
     * @return the property, not null
     */
    public final Property<String> middleName() {
        return metaBean().middleName().createProperty(this);
    }

    //-----------------------------------------------------------------------
    @Override
    public SimpleSubPersonWithBuilderNonFinal clone() {
        return JodaBeanUtils.cloneAlways(this);
    }

    @Override
    public boolean equals(Object obj) {
        if (obj == this) {
            return true;
        }
        if (obj != null && obj.getClass() == this.getClass()) {
            SimpleSubPersonWithBuilderNonFinal other = (SimpleSubPersonWithBuilderNonFinal) obj;
            return JodaBeanUtils.equal(getMiddleName(), other.getMiddleName()) &&
                    super.equals(obj);
        }
        return false;
    }

    @Override
    public int hashCode() {
        int hash = 7;
        hash = hash * 31 + JodaBeanUtils.hashCode(getMiddleName());
        return hash ^ super.hashCode();
    }

    @Override
    public String toString() {
        StringBuilder buf = new StringBuilder(64);
        buf.append("SimpleSubPersonWithBuilderNonFinal{");
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
        buf.append("middleName").append('=').append(JodaBeanUtils.toString(getMiddleName())).append(',').append(' ');
    }

    //-----------------------------------------------------------------------
    /**
     * The meta-bean for {@code SimpleSubPersonWithBuilderNonFinal}.
     */
    public static class Meta extends SimplePersonWithBuilderNonFinal.Meta {
        /**
         * The singleton instance of the meta-bean.
         */
        static final Meta INSTANCE = new Meta();

        /**
         * The meta-property for the {@code middleName} property.
         */
        private final MetaProperty<String> middleName = DirectMetaProperty.ofReadWrite(
                this, "middleName", SimpleSubPersonWithBuilderNonFinal.class, String.class);
        /**
         * The meta-properties.
         */
        private final Map<String, MetaProperty<?>> metaPropertyMap$ = new DirectMetaPropertyMap(
                this, (DirectMetaPropertyMap) super.metaPropertyMap(),
                "middleName");

        /**
         * Restricted constructor.
         */
        protected Meta() {
        }

        @Override
        protected MetaProperty<?> metaPropertyGet(String propertyName) {
            switch (propertyName.hashCode()) {
                case -818219584:  // middleName
                    return middleName;
            }
            return super.metaPropertyGet(propertyName);
        }

        @Override
        public SimpleSubPersonWithBuilderNonFinal.Builder builder() {
            return new SimpleSubPersonWithBuilderNonFinal.Builder();
        }

        @Override
        public Class<? extends SimpleSubPersonWithBuilderNonFinal> beanType() {
            return SimpleSubPersonWithBuilderNonFinal.class;
        }

        @Override
        public Map<String, MetaProperty<?>> metaPropertyMap() {
            return metaPropertyMap$;
        }

        //-----------------------------------------------------------------------
        /**
         * The meta-property for the {@code middleName} property.
         * @return the meta-property, not null
         */
        public final MetaProperty<String> middleName() {
            return middleName;
        }

        //-----------------------------------------------------------------------
        @Override
        protected Object propertyGet(Bean bean, String propertyName, boolean quiet) {
            switch (propertyName.hashCode()) {
                case -818219584:  // middleName
                    return ((SimpleSubPersonWithBuilderNonFinal) bean).getMiddleName();
            }
            return super.propertyGet(bean, propertyName, quiet);
        }

        @Override
        protected void propertySet(Bean bean, String propertyName, Object newValue, boolean quiet) {
            switch (propertyName.hashCode()) {
                case -818219584:  // middleName
                    ((SimpleSubPersonWithBuilderNonFinal) bean).setMiddleName((String) newValue);
                    return;
            }
            super.propertySet(bean, propertyName, newValue, quiet);
        }

    }

    //-----------------------------------------------------------------------
    /**
     * The bean-builder for {@code SimpleSubPersonWithBuilderNonFinal}.
     */
    public static class Builder extends SimplePersonWithBuilderNonFinal.Builder {

        private String middleName;

        /**
         * Restricted constructor.
         */
        protected Builder() {
        }

        /**
         * Restricted copy constructor.
         * @param beanToCopy  the bean to copy from, not null
         */
        protected Builder(SimpleSubPersonWithBuilderNonFinal beanToCopy) {
            super(beanToCopy);
            this.middleName = beanToCopy.getMiddleName();
        }

        //-----------------------------------------------------------------------
        @Override
        public Object get(String propertyName) {
            switch (propertyName.hashCode()) {
                case -818219584:  // middleName
                    return middleName;
                default:
                    return super.get(propertyName);
            }
        }

        @Override
        public Builder set(String propertyName, Object newValue) {
            switch (propertyName.hashCode()) {
                case -818219584:  // middleName
                    this.middleName = (String) newValue;
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
        public SimpleSubPersonWithBuilderNonFinal build() {
            return new SimpleSubPersonWithBuilderNonFinal(this);
        }

        //-----------------------------------------------------------------------
        /**
         * Sets the middle name.
         * @param middleName  the new value
         * @return this, for chaining, not null
         */
        public Builder middleName(String middleName) {
            this.middleName = middleName;
            return this;
        }

        //-----------------------------------------------------------------------
        @Override
        public String toString() {
            StringBuilder buf = new StringBuilder(64);
            buf.append("SimpleSubPersonWithBuilderNonFinal.Builder{");
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
            buf.append("middleName").append('=').append(JodaBeanUtils.toString(middleName)).append(',').append(' ');
        }

    }

    //-------------------------- AUTOGENERATED END --------------------------
}
